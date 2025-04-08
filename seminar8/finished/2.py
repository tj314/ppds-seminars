"""This module implements a scalar product of two vectors using MPI.

The two vectors are randomly generated and then scattered between
processors. The final result is calculated by gathering the partial
results and summing them up on the root processor.
"""

__author__ = "Tomáš Vavro, Marián Šebeňa"
__licence__ = "MIT"

from mpi4py import MPI
import numpy as np

N = 8  # number of elements in the vectors


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

# gather the results
result_array = np.array([result], dtype=np.float64)
total_result = np.empty(world_size, dtype=np.float64)
world.Gather(result_array, total_result, root=0)

if rank == 0:
    print(f"Computed dot product: {total_result.sum()}")
    print(f"Expected dot product: {np.dot(a, b)}")
