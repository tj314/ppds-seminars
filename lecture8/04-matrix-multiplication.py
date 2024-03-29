from numba import cuda
import numpy
import math


@cuda.jit
def matmul(A, B, C):
    row, col = cuda.grid(2)
    if row < C.shape[0] and col < C.shape[1]:
        tmp = 0.0
        for k in range(A.shape[1]):
            tmp += A[row, k] * B[k, col]
        C[row, col] = tmp


A = numpy.full((24, 12), 3, numpy.float32)
B = numpy.full((12, 22), 4, numpy.float32)

A_global_mem = cuda.to_device(A)
B_global_mem = cuda.to_device(B)

C_global_mem = cuda.device_array((24, 22))

threadsperblock = (16, 16)
blockspergrid_x = int(math.ceil(A.shape[0] / threadsperblock[0]))
blockspergrid_y = int(math.ceil(B.shape[1] / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)

matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem)

C = C_global_mem.copy_to_host()

print(C)
