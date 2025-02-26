"""This module implements a solution to the serialization problem.

It is a solution which active waiting.
"""

__author__ = "Tomáš Vavro"

from fei.ppds import Thread, print
from time import sleep


class Shared:
    """This class contains the shared array."""
    def __init__(self, num_threads: int):
        """Initialize the shared array."""
        self.num_threads = num_threads
        self.values = [0, 1] + [0] * num_threads


def fib(tid: int, shared: Shared):
    """Execute the worker thread.

    The first thread doesn't have to wait.
    The second thread has to wait for the first one to finish.
    The third thread has to wait for the second one to finish.
    etc.

    :param tid: integer thread id
    :param shared: shared array and primitives
    """
    while shared.values[tid + 1] == 0:
        sleep(0.1)
    value = shared.values[tid] + shared.values[tid + 1]
    print(f"thread {tid}: {value}")
    shared.values[tid + 2] = value


def main():
    """Create and run threads."""
    num_threads = 5
    sh = Shared(num_threads)
    threads = [Thread(fib, i, sh) for i in range(num_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
