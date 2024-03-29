import math
import numpy
from numba import cuda


@cuda.jit
def my_kernel(io_array):
    pos = cuda.grid(1)
    if pos < io_array.size:
        io_array[pos] *= 2


data_mem = cuda.to_device(numpy.ones(256))
threadsperblock = 32
blockspergrid = int(math.ceil(data_mem.size / threadsperblock))
my_kernel[blockspergrid, threadsperblock](data_mem)
data = data_mem.copy_to_host()
print(data)
