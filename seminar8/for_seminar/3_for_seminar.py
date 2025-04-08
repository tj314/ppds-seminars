"""This module implements a scalar product of two vectors using MPI.

The two vectors are randomly generated and then scattered between
processors. The final result is calculated by employing parallel
reduction.
"""

__author__ = "Tomáš Vavro, Marián Šebeňa, Roderik Ploszek"
__licence__ = "MIT"

from mpi4py import MPI
import numpy as np

N = 101  # number of elements in the vectors


world = MPI.COMM_WORLD
world_size = world.Get_size()
rank = world.Get_rank()

per_processor_range = N // world_size

rng = np.random.default_rng(seed=1)

# initialize the vectors
a = None
b = None
if rank == 0:
    a = rng.random(N)
    b = rng.random(N)
    # pad the arrays to make them divisible by the number of processors
    if N % world_size != 0:
        a = np.pad(a, (0, world_size - N % world_size), mode="constant")
        b = np.pad(b, (0, world_size - N % world_size), mode="constant")

# scatter the data
local_a = np.empty(per_processor_range + (N % world_size != 0), dtype="d")
local_b = np.empty(per_processor_range + (N % world_size != 0), dtype="d")
world.Scatter(a, recvbuf=local_a, root=0)
world.Scatter(b, recvbuf=local_b, root=0)

# calculate the partial dot product
result = np.dot(local_a, local_b)

# TODO: reduce the results (needs a buffer)
# Experiment with data types


if rank == 0:
    print(f"Computed dot product: {total_result[0]}")
    print(f"Expected dot product: {np.dot(a, b)}")
