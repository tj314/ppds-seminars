"""Example 2.5 from Programming in Parallel with CUDA by Richard Ansorge"""
import numpy
from numba import cuda
import sys
import math
from timer import Timer


@cuda.jit
def reduce0(x, stride):
    tid = cuda.grid(1)
    x[tid] += x[tid + stride]


num_elements = 1 << int(sys.argv[1]) if len(sys.argv) > 1 else 1 << 24
rng = numpy.random.default_rng(1)
a = rng.random(num_elements, dtype=numpy.float32)
a_dev = cuda.to_device(a)

# Reduce on host
tim = Timer()
host_sum = numpy.sum(a)
t1 = tim.lap_ms()

# Reduce on GPU
tim.reset()
stride = num_elements // 2
while stride:
    threads = min(256, stride)
    blocks = max(stride // 256, 1)
    reduce0[blocks, threads](a_dev, stride)
    stride //= 2
cuda.synchronize()
t2 = tim.lap_ms()

gpu_sum = a_dev[0]

print(f"sum of {num_elements} random numbers: host {host_sum:.1f} {t1:.1f} ms\n\
                                GPU {gpu_sum:.1f} {t2:.1f} ms")
