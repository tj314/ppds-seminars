"""This module demonstrates the use of a debugger in a very simple example."""

__authors__ = "Marián Šebeňa, Tomáš Vavro"
__license__ = "MIT"

from time import sleep
from fei.ppds import Thread, print
from random import randint


class Shared:
    """Class Shared is used for sharing a value among multiple threads."""

    def __init__(self):
        """Initializes the value to 0 and creates a mutex."""
        self.value = 0


def complex_computation(value):
    """Simulates a complex computation."""
    sleep(randint(1, 10) / 10)  # Simulate a long operation
    return value + 1


def update_value(shared, tid):
    """Updates the value of the shared object."""

    # set a breakpoint on the line 32, then run the debugger
    # step into the complex_computation function
    # then switch to the next thread and compare "value" parameters
    # it should be clear what the problem is :)
    shared.value = complex_computation(shared.value)
    print(f'Thread {tid} has value {shared.value}.')


def main():
    """Creates a shared object and multiple threads that update the value."""
    n_threads = 4
    shared = Shared()
    threads = [Thread(update_value, shared, i) for i in range(n_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
