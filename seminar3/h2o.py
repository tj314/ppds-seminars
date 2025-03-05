"""This module implements the solution to the H2O problem."""

__author__ = "Tomáš Vavro"

from random import randint, choice
from time import sleep
from fei.ppds import Thread, Mutex, Semaphore, print


class Shared:
    """This class contains the shared data."""
    def __init__(self):
        self.h = 0
        self.o = 0
        self.hydro = Semaphore(0)
        self.oxy = Semaphore(0)
        self.mutex = Mutex()

        # you must provide an implementation of the barrier yourself
        self.barrier = ReusableBarrier(3)


def bond(tid: str):
    """Simulate bondage.

    Not *that* kind of bondage...
    """
    sleep(randint(1, 5) / 10.0)
    print(f"thread {tid} contributed to form an H2O molecule!")


def oxygen(tid: int, shared: Shared):
    """Simulate oxygen."""
    print(f"Oxygen {tid} runs!")
    shared.mutex.lock()
    shared.o += 1
    if shared.h < 2:
        shared.mutex.unlock()
    else:
        shared.o -= 1
        shared.h -= 2
        shared.oxy.signal()
        shared.hydro.signal(2)
        # can the unlock be here? ...
        shared.mutex.unlock()
    shared.oxy.wait()
    bond(f"O{tid}")
    shared.barrier.wait()
    # ... or should it be here?
    # shared.mutex.unlock()


def hydrogen(tid: int, shared: Shared):
    """Simulate hydrogen."""
    print(f"Hygrogen {tid} runs!")
    shared.mutex.lock()
    shared.h += 1
    if shared.o < 1 or shared.h < 2:
        shared.mutex.unlock()
    else:
        shared.o -= 1
        shared.h -= 2
        shared.oxy.signal()
        shared.hydro.signal(2)
        shared.mutex.unlock()

    shared.hydro.wait()
    bond(f"H{tid}")
    shared.barrier.wait()

def main():
    """Create threads ad infinitum.

    P(oxygen is created) = 1/3
    P(hydrogen is created) = 2/3
    """
    shared = Shared()
    tid = 0
    while True:
        sleep(0.1)
        if choice([0,1,2]) == 0:
            Thread(oxygen, tid, shared)
        else:
            Thread(hydrogen, tid, shared)
        tid += 1

if __name__ == "__main__":
    main()
