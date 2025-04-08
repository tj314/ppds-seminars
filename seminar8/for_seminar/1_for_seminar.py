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

# TODO: Create a random generator

# initialize the vectors and calculate workflows
if rank == 0:
    # TODO: Generate random arrays a and b

    # TODO: calculate the workload for each processor

    # calculate the expected dot product in order to verify the result
    expected_dot_product = np.dot(a, b)
else:
    # TODO: Prepare buffers for receiving processes

    expected_dot_product = None

# TODO: broadcast the data two vectors and the workloads

# calculate the partial dot product
start = np.sum(processor_ranges[:rank])
result = 0
for i in range(start, start + processor_ranges[rank]):
    result += a[i] * b[i]

# TODO: Wait until computations are finished

# TODO: reduce the results (needs a buffer)

if rank == 0:
    print(f"Computed dot product: {total_result[0]}")
    print(f"Expected dot product: {expected_dot_product}")
