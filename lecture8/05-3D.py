"""Example 2.3 from Programming in Parallel with CUDA by Richard Ansorge"""
import numpy
from numba import cuda
import sys
import math


@cuda.jit
def grid_3d(a, b, id_num):
    nz, ny, nx = a.shape
    x, y, z = cuda.grid(3)
    if x >= nx or y >= ny or z >= nz:
        return

    tx, ty, tz = cuda.threadIdx.x, cuda.threadIdx.y, cuda.threadIdx.z
    bx, by, bz = cuda.blockIdx.x, cuda.blockIdx.y, cuda.blockIdx.z
    bdimx, bdimy, bdimz = cuda.blockDim.x, cuda.blockDim.y, cuda.blockDim.z
    gdimx, gdimy, gdimz = cuda.gridDim.x, cuda.gridDim.y, cuda.gridDim.z

    block_size = bdimx * bdimy * bdimz
    grid_size = gdimx * gdimy * gdimz
    total_threads = block_size * grid_size

    thread_rank_in_block = (tz * bdimy + ty) * bdimx + tx
    block_rank_in_grid = (bz * gdimy + by) * gdimx + bx
    thread_rank_in_grid = block_rank_in_grid * block_size + thread_rank_in_block

    a[z][y][x] = thread_rank_in_grid
    b[z][y][x] = math.sqrt(a[z][y][x])

    if thread_rank_in_grid == id_num:
        print("array size  ", nx, 'x', ny, 'x', nz, '=', a.size)
        print("thread block", bdimx, "x", bdimy, "x", bdimz, "=", block_size)
        print("thread  grid", gdimx, "x", gdimy, "x", gdimz, "=", grid_size)
        print("total number of threads in grid ", total_threads)
        print("a[", z, "][", y, "][", x, "] =", a[z][y][x],
              "and b[", z, "][", y, "][", x, "] =", b[z][y][x])
        print(
            "rank_in_block =",
            thread_rank_in_block,
            " rank_in_grid =",
            thread_rank_in_grid,
            " rank of block_rank_in_grid =",
            block_rank_in_grid,
        )


a = cuda.to_device(numpy.zeros((256, 512, 512), int))
b = cuda.to_device(numpy.zeros((256, 512, 512), numpy.float32))

id_num = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
threadsperblock = 32, 8, 2
blockspergrid = 16, 64, 128
grid_3d[blockspergrid, threadsperblock](a, b, id_num)
