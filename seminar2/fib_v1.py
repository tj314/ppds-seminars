"""This module implements a solution to the serialization problem.

It is a naive solution to the problem involving very ugly,
asymmetric code for the threads.
"""

__author__ = "Tomáš Vavro"

from fei.ppds import Thread, Semaphore, print


class Shared:
    """This class contains the shared array and sync primitives."""
    def __init__(self, num_threads: int):
        """Initialize the shared array and sync primitives."""
        self.num_threads = num_threads
        self.values = [0, 1] + [0] * num_threads
        self.semaphores = [Semaphore(0) for _ in range(num_threads)]


def fib(tid: int, shared: Shared):
    """Execute the worker thread.

    The first thread doesn't have to wait.
    The second thread has to wait for the first one to finish.
    The third thread has to wait for the first
    and the second one to finish.
    etc.
    The last thread and the second to last thread
    do not have to signal two threads.

    :param tid: integer thread id
    :param shared: shared array and primitives
    """
    if tid == 0:
        value = shared.values[tid] + shared.values[tid + 1]
        print(f"thread {tid}: {value}")
        shared.values[tid + 2] = value
        shared.semaphores[1].signal()
        shared.semaphores[2].signal()
    elif tid == 1:
        shared.semaphores[1].wait()
        value = shared.values[tid] + shared.values[tid + 1]
        print(f"thread {tid}: {value}")
        shared.values[tid + 2] = value
        shared.semaphores[2].signal()
        shared.semaphores[3].signal()
    elif tid == shared.num_threads - 2:
        shared.semaphores[tid].wait()
        shared.semaphores[tid].wait()
        value = shared.values[tid] + shared.values[tid + 1]
        print(f"thread {tid}: {value}")
        shared.values[tid + 2] = value
        shared.semaphores[tid + 1].signal()
    elif tid == shared.num_threads - 1:
        shared.semaphores[tid].wait()
        shared.semaphores[tid].wait()
        value = shared.values[tid] + shared.values[tid + 1]
        print(f"thread {tid}: {value}")
        shared.values[tid + 2] = value
    else:
        shared.semaphores[tid].wait()
        shared.semaphores[tid].wait()
        value = shared.values[tid] + shared.values[tid + 1]
        print(f"thread {tid}: {value}")
        shared.values[tid + 2] = value
        shared.semaphores[tid + 1].signal()
        shared.semaphores[tid + 2].signal()


def main():
    """Create and run threads."""
    num_threads = 5
    sh = Shared(num_threads)
    threads = [Thread(fib, i, sh) for i in range(num_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
