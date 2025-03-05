"""This module implements the solution with a single cook."""

__author__ = "Tomáš Vavro"

from fei.ppds import Thread, Semaphore, Mutex, print
from random import randint
from time import sleep
from treebarrier import TreeBarrier


class Shared:
    """This class contains the shared pot and sync objects."""
    def __init__(self, servings_increment, num_savages):
        self.servings_increment = servings_increment
        self.num_servings = 0
        self.mutex = Mutex()
        self.barrier = TreeBarrier(num_savages)
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)


def cook(shared: Shared):
    """Simulates the cook."""
    while True:
        shared.empty_pot.wait()
        sleep(randint(1,5)/10.0)
        shared.num_servings += shared.servings_increment
        print(f"Cook has finished cooking!")
        shared.full_pot.signal()

def savage(tid: int, shared: Shared):
    """Simulates the savage."""
    while True:
        shared.barrier.wait(tid)
        shared.mutex.lock()
        if shared.num_servings == 0:
            shared.empty_pot.signal()
            shared.full_pot.wait()
        shared.num_servings -= 1
        print(f"Savage {tid} took a serving")
        shared.mutex.unlock()
        sleep(randint(1,5)/10.0)
        print(f"Savage {tid} ate his serving")


def main():
    """Create the cook and savages."""
    servings_increment = 10
    num_savages = 3
    shared = Shared(servings_increment, num_savages)
    threads = [Thread(cook, shared)] + [Thread(savage, tid, shared) for tid in range(num_savages)]
    [t.join() for t in threads]

if __name__ == '__main__':
    main()
