"""This module implements a solution to the dining philosophers problem.

The solution in this module is incorrect and results in a deadlock.
"""

__author__ = "Tomáš Vavro"

from fei.ppds import Thread, Semaphore, print
from time import sleep
from random import randint


class Shared:
    """This class represents the shared resources."""
    def __init__(self, num_philosophers: int = 5):
        """Initialize the shared resources."""
        self.forks = [Semaphore(1) for _ in range(num_philosophers)]
        self.num_philosophers = num_philosophers
        self.waiter = Semaphore(num_philosophers - 1)


def philosopher(tid: int, shared: Shared):
    """Execute the philosopher routine."""
    while True:
        # think
        print(f"philosopher {tid} is thinking")
        sleep(randint(1, 5) / 10.0)

        # eat
        shared.waiter.wait()
        shared.forks[tid].wait()
        shared.forks[(tid + 1) % shared.num_philosophers].wait()
        print(f"philosopher {tid} is eating")
        sleep(randint(1, 5) / 10.0)
        shared.forks[tid].signal()
        shared.forks[(tid + 1) % shared.num_philosophers].signal()
        shared.waiter.signal()


def main():
    """Execute the main routine."""
    num_philosophers = 5
    shared = Shared(num_philosophers)
    threads = [Thread(philosopher, tid, shared)
               for tid in range(num_philosophers)]
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
