"""Example 2.7 from Programming in Parallel with CUDA by Richard Ansorge"""
import numpy
from numba import cuda, float32
import sys
import math
from timer import Timer


@cuda.jit
def reduce2(y, x, num_elements):
    _id = cuda.threadIdx.x
    tid = cuda.grid(1)
    stride = cuda.gridDim.x * cuda.blockDim.x
    tsum = cuda.shared.array(0, dtype=float32)
    tsum[_id] = 0.0
    for k in range(tid, num_elements, stride):
        tsum[_id] += x[k]
    cuda.syncthreads()
    k = cuda.blockDim.x // 2
    while k > 0:
        if _id < k:
            tsum[_id] += tsum[_id + k]
        cuda.syncthreads()
        k //= 2
    if _id == 0:
        y[cuda.blockIdx.x] = tsum[0]


num_elements = 1 << int(sys.argv[1]) if len(sys.argv) > 1 else 1 << 24
blocks = int(sys.argv[2]) if len(sys.argv) > 2 else 256
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 256

rng = numpy.random.default_rng(12345678)
dx = rng.random(num_elements, numpy.float32)
dx_dev = cuda.to_device(dx)
dy_dev = cuda.to_device(numpy.zeros(blocks, numpy.float32))

# Reduce on host
tim = Timer()
host_sum = numpy.sum(dx)
t1 = tim.lap_ms()

# Reduce on GPU
tim.reset()
reduce2[blocks, threads, 0, threads * dx_dev.dtype.itemsize](
    dy_dev, dx_dev, num_elements
)
reduce2[1, blocks, 0, blocks * dy_dev.dtype.itemsize](dx_dev, dy_dev, blocks)
cuda.synchronize()
t2 = tim.lap_ms()

gpu_sum = dx_dev[0]

print(
    f"sum of {num_elements} random numbers: host {host_sum:.1f} {t1:.1f} ms\n\
                                GPU {gpu_sum:.1f} {t2:.1f} ms"
)
