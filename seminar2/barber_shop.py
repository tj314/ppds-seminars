"""
Program for educational purpose. (Barber Shop)

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""


__authors__ = "Marián Šebeňa"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread
from time import sleep
from random import randint


class Shared(object):

    def __init__(self):

        # TODO : Initialize patterns we need and variables
        self.mutex = Mutex()
        self.waiting_room = 0
        # self.customer = Rendezvous is implemented as ?
        # self.barber = Rendezvous is implemented as ?
        # self.customer_done = Rendezvous is implemented as ?
        # self.barber_done = Rendezvous is implemented as ?


def get_haircut(i):
    # TODO: Simulate time and print info when customer gets haircut
    pass


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    pass


def balk(i):
    # TODO: Represents situation when waiting room is full and print info
    pass


def growing_hair(i):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is sleeping for some time
    pass


def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)

        # TODO: Rendezvous 1
        get_haircut(i)
        # TODO: Rendezvous 2

        # TODO: Leave waiting room. Integrity again
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()

# TODO: Global variables C = 5 numOfCustomers N = 3 sizeOfWaitingRoom


if __name__ == "__main__":
    main()
