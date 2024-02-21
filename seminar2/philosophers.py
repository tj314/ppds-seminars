"""
Program for educational purpose. (Dining philosophers)

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
        self.num_philosophers = num_philosophers
        self.forks = [Semaphore(1) for _ in range(num_philosophers)]


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
        think(tid)
        shared.forks[tid].wait()
        shared.forks[(tid + 1) % shared.num_philosophers].wait()
        eat(tid)
        shared.forks[tid].signal()
        shared.forks[(tid + 1) % shared.num_philosophers].signal()


def main():
    """Main function."""
    num_philosophers = 5
    shared = Shared(num_philosophers)
    threads = [Thread(philosopher, shared, i) for i in range(num_philosophers)]
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
