from fei.ppds import Thread, Semaphore
from time import sleep
from random import randint

# todo: implement a suitable barrier (tree, simple, reusable...)
#       you may implement it here or (preferably) in a separate file


class Shared:
    def __init__(self, train_capacity, num_passengers):
        self.train_capacity = train_capacity
        self.num_passengers = num_passengers


def car(shared):
    while True:
        # todo: signal to the passengers that they can board
        # todo: wait for the passengers to board and
        #       do not start the ride unless the capacity is satisfied
        print(f"the car is on the ride")
        # does it make sense for a ride to be of random variable duration?
        sleep(randint(1, 3) / 10.0)
        # todo: signal to the passengers that they may leave
        # todo: wait for all the passengers to leave


def passenger(shared, tid):
    while True:
        # todo: wait for the car to arrive
        # todo: board the car and signal to it
        #       once all of the passengers have boarded
        print(f"the passenger {tid} is enjoying the ride")
        sleep(randint(1, 3) / 10.0)
        # todo: wait for the car to finish the ride
        # todo: leave the car and signal to it once
        #       all of the passengers have left


def main():
    shared = Shared(5, 10)
    threads = [Thread(car, shared)] +\
              [Thread(passenger, shared, i)
               for i in range(shared.num_passengers)]
    [t.join() for t in threads]