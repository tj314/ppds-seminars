"""Running multiple kernels on the GPU sequentially."""

from numba import cuda
import numpy as np
from time import perf_counter


NUM_ARRAYS = 200
ARRAY_LEN = 2**20


@cuda.jit
def kernel(array):
    """Do some dummy operations on an array.

    :param array: array where the operations will be done. Should be
    left with the same values after the kernel is done.
    """
    thd = cuda.grid(1)
    num_iters = array.size // cuda.blockDim.x
    for j in range(num_iters):
        i = j * cuda.blockDim.x + thd
        for k in range(50):
            array[i] *= 2
            array[i] /= 2


data = []
data_gpu = []
gpu_out = []

for _ in range(NUM_ARRAYS):
    data.append(np.random.randn(ARRAY_LEN).astype('float32'))

t_start = perf_counter()

for array in data:
    data_gpu.append(cuda.to_device(array))

for array in data_gpu:
    kernel[1, 64](array)

for array in data_gpu:
    gpu_out.append(array.copy_to_host())

t_end = perf_counter()

# Check if the arrays are the same (within a small floating point error)
for gpu_array, array in zip(gpu_out, data):
    assert np.allclose(gpu_array, array)

print(f'Total time: {t_end - t_start:.2f}')
