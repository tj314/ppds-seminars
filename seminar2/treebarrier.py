"""This module implements a tree barrier."""

__author__ = "Tomáš Vavro"

import math

from fei.ppds import Thread, Semaphore, print, Event


class TreeBarrier:
    """This class implements a tree barrier.

    It is assumed that the number of threads is a power of 2.
    """
    def __init__(self, num_threads: int):
        """Initialize the tree barrier."""
        if not math.log2(num_threads).is_integer():
            raise ValueError("num_threads must be a power of 2.")
        self.num_threads = num_threads
        self.in_semaphores = [Semaphore(0) for _ in range(num_threads)]
        self.out_semaphores = [Semaphore(0) for _ in range(num_threads)]

    def wait(self, tid):
        """Wait at the barrier."""
        if 2 * tid + 1 >= self.num_threads:
            # this node is a leaf
            self.in_semaphores[tid].signal()
            self.out_semaphores[tid].wait()
        elif tid == 0:
            # this node is the root
            self.in_semaphores[2 * tid + 1].wait()
            self.in_semaphores[2 * tid + 2].wait()
            self.out_semaphores[2 * tid + 1].signal()
            self.out_semaphores[2 * tid + 2].signal()
        else:
            self.in_semaphores[2 * tid + 1].wait()
            self.in_semaphores[2 * tid + 2].wait()
            self.in_semaphores[tid].signal()
            self.out_semaphores[tid].wait()
            self.out_semaphores[2 * tid + 1].signal()
            self.out_semaphores[2 * tid + 2].signal()


class Shared:
    """This class implements a shared object."""
    def __init__(self, num_threads):
        """Initialize the shared object."""
        self.num_threads = num_threads
        self.barrier = TreeBarrier(num_threads)


def worker(tid: int, shared: Shared):
    """Wait for the barrier and notify after passing through."""
    print(f"worker {tid} is before the barrier")
    shared.barrier.wait(tid)
    print(f"worker {tid} is after the barrier")


def main():
    """Execute the main routine."""
    num_threads = 7
    shared = Shared(num_threads)
    threads = [Thread(worker, i, shared) for i in range(num_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
