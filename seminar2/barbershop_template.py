from fei.ppds import Mutex, Thread, print
from time import sleep
from random import randint


class BarberShop(object):
    def __init__(self, C: int = 5, N: int = 3):
        self.C = C  # number of customers
        self.N = N  # capacity of the waiting room
        # TODO: Initialize the synchronization primitives we need
        # TODO: Initialize any necessary variables

def get_haircut(tid):
    print(f"customer {tid} is getting hair cut")
    sleep(0.1)


def cut_hair():
    print(f"barber is cutting the hair")
    sleep(0.2)


def leave_full_barbershop(tid):
    print(f"barbershop is full, customer {tid} leaves")


def growing_hair(tid):
    print(f"customer {tid}'s hair is growing")
    sleep(0.2)


def customer(i, shared):
    # TODO: Function represents customers behaviour.
    #       Customers come to the waiting room.
    #       if it is full, they leave.
    # TODO: Wake up barber if necessary
    #       and wait for invitation from him. Then get new haircut.
    # TODO: Both the customer and the barber must wait
    #       to complete their work. After getting the haircut,
    #       the customer leaves and waits for the hair to grow again.

    while True:
        # TODO: Access to waiting room.
        #       Can the customer enter or must he wait?
        #       Be careful about counter integrity :)

        # TODO: Rendezvous 1
        get_haircut(i)
        # TODO: Rendezvous 2

        # TODO: Leave the waiting room. Integrity again.
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents the barber.
    #       Initially, the barber is sleeping.
    # TODO: When customer arrives to get new haircut,
    #       he wakes up barber.
    # TODO: Barber cuts customer's hair.
    #       They must both wait to complete their work.
    # TODO: If there is no customer, the barber sleeps.

    while True:
        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


def main():
    barbershop = BarberShop()
    customers = []

    for i in range(barbershop.C):
        customers.append(Thread(customer, i, barbershop))
    hair_stylist = Thread(barber, barbershop)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()