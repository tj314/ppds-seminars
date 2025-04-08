"""A ping-pong program in python, using pickle'd communication.

This program file is part of the book and course
"Parallel Computing"
by Victor Eijkhout, copyright 2013-5
"""

from mpi4py import MPI
import time

comm = MPI.COMM_WORLD

ntids = comm.Get_size()
mytid = comm.Get_rank()
ntests = 100

for s in [1, 10, 100, 1000, 10000, 100000, 1000000]:
    # snippet pingpongp
    if mytid == 0:
        data = [2.0 * i for i in range(s)]
        starttime = MPI.Wtime()
        for _ in range(ntests):
            comm.send(data, dest=ntids - 1)
            rdata = comm.recv(source=ntids - 1)
        elapsed = MPI.Wtime() - starttime
        print(f"Size={s}, elapsed time: {elapsed}")

        # Show that this won't work with numpy
        if data != rdata:
            print("oops", data, rdata)
    elif mytid == ntids - 1:
        for _ in range(ntests):
            zdata = comm.recv(source=0)
            comm.send(zdata, dest=0)
            # snippet end
