"""Example 2.7 from Programming in Parallel with CUDA."""

__authors__ = "Richard Ansorge, Roderik Ploszek"
__license__ = "GPL-2.0-only"

import numpy
from numba import cuda, float32
import sys
from timer import Timer


@cuda.jit
def reduce2(y, x, num_elements):
    """Compute partial summing reduction of `x`.

    Partial sums of each block are stored in y[0 : NUM_BLOCKS - 1].
    When the number of threads is the same as number of blocks, the
    final sum is stored in y[0].

    :param y: Output helper array. Needs to have as many elements as
    there are blocks in the computation.
    :param x: Array to be summed.
    :param num_elements: Size of `x`.
    """
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

tim = Timer()
host_times = numpy.array([], dtype=numpy.uint64)
device_times = numpy.array([], dtype=numpy.uint64)

# Reduce on host
for _ in range(100):
    tim.reset()
    host_sum = numpy.sum(dx)
    # host_sum = sum(a)
    t1 = tim.lap_ms()
    host_times = numpy.append(host_times, t1)

# Reduce on GPU
for _ in range(100):
    dy_dev = cuda.to_device(numpy.zeros(blocks, numpy.float32))
    tim.reset()
    reduce2[blocks, threads, 0, threads * dx_dev.dtype.itemsize](
        dy_dev, dx_dev, num_elements
    )
    reduce2[1, blocks, 0, blocks * dy_dev.dtype.itemsize](
        dx_dev, dy_dev, blocks
    )
    cuda.synchronize()
    t2 = tim.lap_ms()
    device_times = numpy.append(device_times, t2)
gpu_sum = dx_dev[0]

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
print(f"{host_time_median:.2f}±{host_time_std:.3f} ms")

print(f"                                GPU  {gpu_sum:.1f}  ", end='')
print(f"{device_time_median:.2f}±{device_time_std:.3f} ms")
