"""CUDA Stream-based Concurrent Conway's game of life in Python / CUDA.

Written by Brian Tuomanen for "Hands on GPU Programming with Python and
CUDA".
Converted to numba by Roderik Ploszek.
"""

__authors__ = "Brian Tuomanen, Roderik Ploszek"
__license__ = "MIT"

from numba import cuda
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


@cuda.jit(device=True)
def nbrs(x, y, matrix):
    """Compute sum of the 8 neighboring elements.

    :param x: x position of the element from which to take the neighbors
    :param y: y position of the element from which to take the neighbors
    :param matrix: matrix to take values from
    :returns: sum of the 8 neighboring elements of element matrix[x, y]
    """
    return (
        matrix[x - 1, y + 1]
        + matrix[x - 1, y]
        + matrix[x - 1, y - 1]
        + matrix[x, y + 1]
        + matrix[x, y - 1]
        + matrix[x + 1, y - 1]
        + matrix[x + 1, y]
        + matrix[x + 1, y + 1]
    )


@cuda.jit
def kernel(lattice_out, lattice):
    """Compute a new state of the game board.

    :param lattice_out: output matrix, has the same shape as `lattice`
    :param lattice: input array, has the same shape as `lattice_out`
    """
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


def update_gpu(frame_num, imgs, new_lattices_gpu, lattices_gpu, n, streams):
    """Compute a new state of the game board on the GPU and get it back.

    This is a callback function used by
    matplotlib.animation.FuncAnimation.

    :param frame_num: Frame number, not used.
    :param img: AxesImage object, where the board is drawn.
    :param new_lattice_gpu: Square matrix of size `n` used to draw the
    values.
    :param lattice_gpu: Square matrix of size `n` used to store the
    previous state of the board.
    :param n: Size of the square matrices new_lattice_gpu and
    lattice_gpu.
    :param streams: List of cuda streams where kernels will be executed.
    """
    blockdim = (n // 32, n // 32)
    griddim = (32, 32)
    for stream, new_lattice_gpu, lattice_gpu, img in zip(
        streams, new_lattices_gpu, lattices_gpu, imgs
    ):
        kernel[griddim, blockdim, stream](new_lattice_gpu, lattice_gpu)

        img.set_data(new_lattice_gpu.copy_to_host(stream=stream))

        lattice_gpu.copy_to_device(new_lattice_gpu, stream=stream)


N = 128
NUM_CONCURRENT = 4

streams = []
lattices_gpu = []
new_lattices_gpu = []

for _ in range(NUM_CONCURRENT):
    streams.append(cuda.stream())
    lattice = np.int32(
        np.random.choice([1, 0], N * N, p=[0.25, 0.75]).reshape(N, N)
    )

    lattice_gpu = cuda.to_device(lattice)
    lattices_gpu.append(lattice_gpu)

    new_lattice_gpu = cuda.device_array_like(lattice_gpu)
    new_lattices_gpu.append(new_lattice_gpu)

fig, ax = plt.subplots(nrows=1, ncols=NUM_CONCURRENT)
imgs = []

for window, lattice_gpu, stream in zip(ax, lattices_gpu, streams):
    imgs.append(
        window.imshow(
            lattice_gpu.copy_to_host(stream=stream), interpolation='nearest'
        )
    )

ani = animation.FuncAnimation(
    fig,
    update_gpu,
    fargs=(imgs, new_lattices_gpu, lattices_gpu, N, streams),
    interval=33,
    frames=1000,
)
plt.show()
