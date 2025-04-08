"""A ping-pong program in python, using numpy communication.

This program file is part of the book and course
"Parallel Computing"
by Victor Eijkhout, copyright 2013-5
"""

from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD

ntids = comm.Get_size()
mytid = comm.Get_rank()
ntests = 100

for s in [1, 10, 100, 1000, 10000, 100000, 1000000]:
    # snippet pingpongpp
    if mytid == 0:
        data = np.arange(s, dtype=np.float64)
        rdata = np.empty(s, dtype=np.float64)
        for i in range(s):
            data[i] = i + 1
        starttime = MPI.Wtime()
        for test in range(ntests):
            comm.Send([data, MPI.DOUBLE], dest=ntids - 1)
            comm.Recv([rdata, MPI.DOUBLE], source=ntids - 1)
        elapsed = MPI.Wtime() - starttime
        print(f"Size={s}, elapsed time: {elapsed}")
        if not np.array_equal(data, rdata):
            print("oops", data, rdata)
    elif mytid == ntids - 1:
        zdata = np.empty(s, dtype=np.float64)
        for test in range(ntests):
            comm.Recv([zdata, MPI.DOUBLE], source=0)
            comm.Send([zdata, MPI.DOUBLE], dest=0)
            # snippet end
