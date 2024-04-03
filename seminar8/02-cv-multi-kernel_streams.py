from numba import cuda
import numpy as np
from time import perf_counter


NUM_ARRAYS = 200
ARRAY_LEN = 1024**2


@cuda.jit
def kernel(array):
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
streams = []

for _ in range(NUM_ARRAYS):
    streams.append(cuda.stream())
    data.append(np.random.randn(ARRAY_LEN).astype('float32'))

t_start = perf_counter()

for array, stream in zip(data, streams):
    data_gpu.append(cuda.to_device(array, stream=stream))

for array, stream in zip(data_gpu, streams):
    kernel[1, 64, stream](array)

for array, stream in zip(data_gpu, streams):
    gpu_out.append(array.copy_to_host(stream=stream))

t_end = perf_counter()

for gpu_array, array in zip(gpu_out, data):
    assert(np.allclose(gpu_array, array))

print(f'Total time: {t_end - t_start:.2f}')
