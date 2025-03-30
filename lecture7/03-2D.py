"""CUDA kernel on 2D array."""

import numpy
from numba import cuda
import math


@cuda.jit
def my_kernel(io_array):
    """Multiply each element of `io_array` by 2 on GPU.

    :param io_array: Elements from this array are replaced by the
    resulting products.
    """
    x, y = cuda.grid(2)
    y_max, x_max = io_array.shape
    if x < x_max and y < y_max:
        io_array[y, x] *= 2


data_mem = cuda.to_device(numpy.ones((16, 16)))
threadsperblock = (5, 5)
blockspergrid_x = int(math.ceil(data_mem.shape[0] / threadsperblock[0]))
blockspergrid_y = int(math.ceil(data_mem.shape[1] / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)
my_kernel[blockspergrid, threadsperblock](data_mem)
data = data_mem.copy_to_host()
print(data)
