"""This module implements a scalar product of two vectors using MPI.

The two vectors are randomly generated and then broadcast to all
processors. This solution is not optimal, as the data is broadcasted to
all processors, even though only a part of it is needed.
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

# initialize the vectors and calculate workflows
if rank == 0:
    a = rng.random(N)
    b = rng.random(N)
    # calculate the workload for each processor
    processor_ranges = np.array(
        [per_processor_range for _ in range(world_size)], dtype=np.int32
    )
    for i in range(N % world_size):
        processor_ranges[i] += 1
    # calculate the expected dot product in order to verify the result
    expected_dot_product = np.dot(a, b)
else:
    a = np.empty(N, dtype=np.float64)
    b = np.empty(N, dtype=np.float64)
    processor_ranges = np.empty(world_size, dtype=np.int32)
    expected_dot_product = None

# broadcast the data two vectors and the workloads
world.Bcast([a, MPI.DOUBLE], root=0)
world.Bcast([b, MPI.DOUBLE], root=0)
world.Bcast([processor_ranges, MPI.INT], root=0)

# calculate the partial dot product
start = np.sum(processor_ranges[:rank])
result = 0
for i in range(start, start + processor_ranges[rank]):
    result += a[i] * b[i]

# is the barrier necessary?
# world.Barrier()

# reduce the results
total_result = np.zeros(1, dtype=np.float64)
world.Reduce(result, total_result, op=MPI.SUM)

if rank == 0:
    print(f"Computed dot product: {total_result[0]}")
    print(f"Expected dot product: {expected_dot_product}")
