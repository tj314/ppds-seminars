"""Example 2.5 from Programming in Parallel with CUDA."""

__authors__ = "Richard Ansorge, Roderik Ploszek"
__license__ = "GPL-2.0-only"

import numpy
from numba import cuda
import sys
from timer import Timer


@cuda.jit
def reduce0(x, stride):
    """Calculate one step of a summing reduction.

    The offset is determined by `stride`. The function doesn't check for
    overflows!

    :param x: Array to be summed.
    :param stride: Offset of the element to be summed.
    """
    tid = cuda.grid(1)
    x[tid] += x[tid + stride]


num_elements = 1 << int(sys.argv[1]) if len(sys.argv) > 1 else 1 << 24
rng = numpy.random.default_rng(1)
a = rng.random(num_elements, dtype=numpy.float32)
a_dev = cuda.to_device(a)

tim = Timer()
host_times = numpy.array([], dtype=numpy.uint64)
device_times = numpy.array([], dtype=numpy.uint64)

# Reduce on host
for _ in range(100):
    tim.reset()
    host_sum = numpy.sum(a)
    # host_sum = sum(a)
    t1 = tim.lap_ms()
    host_times = numpy.append(host_times, t1)

# Reduce on GPU
for _ in range(100):
    a_dev = cuda.to_device(a)
    tim.reset()
    stride = num_elements // 2
    while stride:
        threads = min(256, stride)
        blocks = max(stride // 256, 1)
        reduce0[blocks, threads](a_dev, stride)
        stride //= 2
    cuda.synchronize()
    t2 = tim.lap_ms()
    device_times = numpy.append(device_times, t2)
gpu_sum = a_dev[0]

# print(host_times)
# print(device_times)

# Remove high outliers (90th percentile)
high_host_time = numpy.percentile(host_times, 90)
host_times = host_times[host_times <= high_host_time]
high_device_time = numpy.percentile(device_times, 90)
device_times = device_times[device_times <= high_device_time]

# Compute median and sample standard deviation
host_time_median = numpy.median(host_times)
host_time_std = numpy.std(host_times, ddof=1)
device_time_median = numpy.median(device_times)
device_time_std = numpy.std(device_times, ddof=1)

print(f"sum of {num_elements} random numbers: host {host_sum:.1f}  ", end='')
print(f"{host_time_median:.1f}±{host_time_std:.2f} ms")

print(f"                                GPU  {gpu_sum:.1f}  ", end='')
print(f"{device_time_median:.1f}±{device_time_std:.2f} ms")
