"""
This module contains an implementation of the h20 problem
"""

__authors__ = "Marián Šebeňa, Matúš Jókay"
__email__ = "mariansebena@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint

# Initializing oxygen's and hydrogen's
OX = 100
HY = 200


class SimpleBarrier(object):
    """
    Implementation of simple barrier
    """
    def __init__(self, n):
        self.N = n
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            self.barrier.signal(self.N)
        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    """
    Shared class for storing sync patterns
    """
    def __init__(self):
        self.mutex = Mutex()
        self.iters = 0
        self.oxygen = 0
        self.hydrogen = 0
        self.oxyQueue = Semaphore(0)
        self.hydroQueue = Semaphore(0)
        self.barrier = SimpleBarrier(3)


def bond(i, name):
    """
    Simulating connection between 1 oxygen and 2 hydrogen
    """
    print(f'{name}{i}:Connecting')
    sleep(randint(1, 2)/10)


def oxygen(i, shared):
    """
    Implementation of oxygen´s functionality
    """
    # TODO: Complete the code from the pseudocode


def hydrogen(i, shared):
    """
    Implementation of hydrogen´s functionality
    """
    # TODO: Complete the code from the pseudocode


def main():
    """
    Thread management and main functionality handling
    """
    shared = Shared()
    ox = []
    hyd = []

    # TODO: Reimplement to generate threads
    for i in range(OX):
        ox.append(Thread(oxygen, i, shared))
    for j in range(HY):
        hyd.append(Thread(hydrogen, j, shared))

    for t in hyd + ox:
        t.join()


if __name__ == "__main__":
    main()