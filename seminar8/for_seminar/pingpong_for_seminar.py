"""A ping-pong program in python, using pickle'd communication.

This program file is part of the book and course
"Parallel Computing"
by Victor Eijkhout, copyright 2013-5
"""

from mpi4py import MPI
import time

# TODO: Get MPI COMM_WORLD object

ntids = 0
mytid = 0

ntests = 100

for s in [1, 10, 100, 1000, 10000, 100000, 1000000]:
    # snippet pingpongp
    if mytid == 0:
        data = [2.0 * i for i in range(s)]
        # TODO: Add timing
        for _ in range(ntests):
            # TODO: Add communication
            rdata = None
            pass
        elapsed = 0
        print(f"Size={s}, elapsed time: {elapsed}")

        # Show that this won't work with numpy
        if data != rdata:
            print("oops", data, rdata)
    elif mytid == ntids - 1:
        for _ in range(ntests):
            # TODO: Add communication
            pass
            # snippet end
