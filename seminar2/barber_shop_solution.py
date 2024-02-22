"""This module contains an implementation of the barber shop with overtaking
problem using rendezvous.
"""

__authors__ = "Marián Šebeňa, Matúš Jókay"
__email__ = "mariansebena@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint

C = 5  # number of customers
N = 3  # size of waiting room


class Shared(object):
    """
    A class that represents shared resources for a barber problem
    simulation.
    """

    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """
    Prints out that customer get a haircut.
    """

    print(f"Customer {i} gets haircut")
    sleep(randint(2, 5)/10)


def cut_hair():
    """
    Prints out that barber cuts customers hair.
    """

    print(f"Barber cuts hair")
    sleep(randint(2, 5)/10)


def balk(i):
    """
    Simulates a situation where the customer try enters full waiting room.
    """

    print(f"Waiting room is full. Customer {i} leaves")
    sleep(randint(2, 5)/10)


def growing_hair(i):
    """
    Simulates a situation where the customer waits for his hair to grow again.
    """

    sleep(randint(2, 5)/10)
    print(f"Customer {i} is ready for another haircut")


def customer(i, shared):
    """
    Simulates a customer behaviour in the barber shop.
    """

    while True:
        # Enter the waiting room
        shared.mutex.lock()
        if shared.waiting_room < N:
            shared.waiting_room += 1
            print(f"Customer {i} enters the waiting room")
            shared.mutex.unlock()
        else:
            shared.mutex.unlock()
            balk(i)
            continue
        # Rendezvous 1
        shared.barber.signal()
        shared.customer.wait()

        get_haircut(i)

        # Rendezvous 2
        shared.customer_done.signal()
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.waiting_room -= 1
        print(f"Customer {i} has left the barber shop")
        shared.mutex.unlock()

        growing_hair(i)


def barber(shared):
    """
    Represents a barber that wait or cut hair depending on the situation.
    """

    while True:
        # Rendezvous 1
        shared.barber.wait()
        shared.customer.signal()

        cut_hair()

        # Rendezvous 2
        shared.customer_done.wait()
        shared.barber_done.signal()


def main():
    """
    Contains main functionality including thread initialization.
    """
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()