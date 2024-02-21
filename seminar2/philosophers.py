"""Program for educational purpose. (Dining philosophers)

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Tomáš Vavro"
__email__ = "tomas.vavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Semaphore, print
from time import sleep
from random import randint


class Shared:
    """Represents shared data."""
    def __init__(self, num_philosophers):
        # TODO: Initialize the forks
        pass


def think(tid):
    """Simulates thinking."""
    sleep(randint(1, 5) / 10)
    print(f"Philosopher {tid} is thinking.")


def eat(tid):
    """Simulates eating."""
    sleep(randint(1, 5) / 10)
    print(f"Philosopher {tid} is eating.")


def philosopher(shared, tid):
    """Simulates a philosopher."""
    while True:
        # TODO: Simulate thinking
        # TODO: Simulate taking the forks
        # TODO: Simulate eating
        # TODO: Simulate putting the forks
        pass


def main():
    """Main function."""
    num_philosophers = 5
    shared = Shared(num_philosophers)
    threads = [Thread(philosopher, shared, i) for i in range(num_philosophers)]
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
