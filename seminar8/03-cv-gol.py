from numba import cuda
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


@cuda.jit(device=True)
def nbrs(x, y, matrix):
    return (matrix[x - 1, y + 1] + matrix[x - 1, y] + matrix[x - 1, y - 1] +
            matrix[x, y + 1] + matrix[x, y - 1] + matrix[x + 1, y - 1] +
            matrix[x + 1, y] + matrix[x + 1, y + 1])


@cuda.jit
def kernel(lattice_out, lattice):
    x, y = cuda.grid(2)
    n = nbrs(x, y, lattice)

    if lattice[x, y] == 1:
        if n in (2, 3):
            lattice_out[x, y] = 1
        else:
            lattice_out[x, y] = 0
    elif lattice[x, y] == 0:
        if n == 3:
            lattice_out[x, y] = 1
        else:
            lattice_out[x, y] = 0


def update_gpu(frame_num, img, new_lattice_gpu, lattice_gpu, N):
    blockdim = (N // 32, N // 32)
    griddim = (32, 32)
    kernel[griddim, blockdim](new_lattice_gpu, lattice_gpu)

    img.set_data(new_lattice_gpu.copy_to_host())

    lattice_gpu[:] = new_lattice_gpu[:]

    return img


N = 128
lattice = np.int32(
    np.random.choice([1, 0], N * N, p=[0.25, 0.75]).reshape(N, N)
)
lattice_gpu = cuda.to_device(lattice)

new_lattice_gpu = cuda.device_array_like(lattice_gpu)

fig, ax = plt.subplots()
img = ax.imshow(lattice_gpu.copy_to_host(), interpolation='nearest')
ani = animation.FuncAnimation(fig,
                              update_gpu,
                              fargs=(
                                  img,
                                  new_lattice_gpu,
                                  lattice_gpu,
                                  N
                              ),
                              interval=33,
                              frames=1000)
plt.show()
