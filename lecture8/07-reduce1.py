"""Example 2.6 from Programming in Parallel with CUDA by Richard Ansorge"""
import numpy
from numba import cuda
import sys
import math
from timer import Timer


@cuda.jit
def reduce1(x, num_elements):
    tid = cuda.grid(1)
    tsum = 0.0
    stride = cuda.gridDim.x * cuda.blockDim.x
    for k in range(tid, num_elements, stride):
        tsum += x[k]
    x[tid] = tsum


num_elements = 1 << int(sys.argv[1]) if len(sys.argv) > 1 else 1 << 24
blocks = int(sys.argv[2]) if len(sys.argv) > 2 else 288
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 256

rng = numpy.random.default_rng(1)
a = rng.random(num_elements, dtype=numpy.float32)
a_dev = cuda.to_device(a)

# Reduce on host
tim = Timer()
host_sum = numpy.sum(a)
t1 = tim.lap_ms()

# Reduce on GPU
tim.reset()
reduce1[blocks, threads](a_dev, a.size)
reduce1[1, threads](a_dev, blocks * threads)
reduce1[1, 1](a_dev, threads)
cuda.synchronize()
t2 = tim.lap_ms()

gpu_sum = a_dev[0]

print(
    f"sum of {num_elements} random numbers: host {host_sum:.1f} {t1:.1f} ms\n\
                                      GPU {gpu_sum:.1f} {t2:.1f} ms"
)
