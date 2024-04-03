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
start_events = []
end_events = []

for _ in range(NUM_ARRAYS):
    streams.append(cuda.stream())
    start_events.append(cuda.event())
    end_events.append(cuda.event())
    data.append(np.random.randn(ARRAY_LEN).astype('float32'))

t_start = perf_counter()

for array, stream in zip(data, streams):
    data_gpu.append(cuda.to_device(array, stream=stream))

for array, stream, event in zip(data_gpu, streams, start_events):
    event.record(stream=stream)
    kernel[1, 64, stream](array)

for stream, event in zip(streams, end_events):
    event.record(stream=stream)

for array, stream in zip(data_gpu, streams):
    gpu_out.append(array.copy_to_host(stream=stream))

t_end = perf_counter()

for gpu_array, array in zip(gpu_out, data):
    assert(np.allclose(gpu_array, array))

kernel_times = []
for start_event, end_event in zip(start_events, end_events):
    kernel_times.append(cuda.event_elapsed_time(start_event, end_event))

print(f'Total time: {t_end - t_start:.2f}')
print(f'Mean kernel duration (milliseconds): {np.mean(kernel_times):.2f}')
print(f'Mean kernel standard deviation (milliseconds): {np.std(kernel_times):.2f}')
