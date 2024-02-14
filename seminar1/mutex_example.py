"""This module implements code examples from the seminar 1."""

__authors__ = "Marián Šebeňa, Tomáš Vavro"
__license__ = "MIT"

from time import sleep

from fei.ppds import Thread, Mutex, print


class Shared:
    """This class represents shared data."""
    def __init__(self, end):
        """Initializes shared data."""
        self.counter = 0
        self.end = end
        self.arr = [0] * end
        self.mutex = Mutex()


def version1(shared, tid):
    """This function implements a correct, but not optimal solution."""
    shared.mutex.lock()
    while shared.counter != shared.end:
        print(f"Thread {tid} - counter: {shared.counter}")
        shared.arr[shared.counter] += 1
        shared.counter += 1
        sleep(1)  # Simulate a long operation
    shared.mutex.unlock()


def version2(shared, tid):
    """This function implements an incorrect solution.

    The problem is that the condition in the while loop is not protected by the mutex."""
    while shared.counter != shared.end:
        shared.mutex.lock()
        print(f"Thread {tid} - counter: {shared.counter}")
        shared.arr[shared.counter] += 1
        shared.counter += 1
        sleep(1)  # Simulate a long operation
        shared.mutex.unlock()


def version3(shared, tid):
    """This function implements another incorrect solution.

    The problem is that the mutex is not unlocked when break executes."""
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            break
        print(f"Thread {tid} - counter: {shared.counter}")
        shared.arr[shared.counter] += 1
        shared.counter += 1
        sleep(1)  # Simulate a long operation
        shared.mutex.unlock()


def version4(shared, tid):
    """This function implements another correct solution."""
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        print(f"Thread {tid} - counter: {shared.counter}")
        shared.arr[shared.counter] += 1
        shared.counter += 1
        sleep(1)  # Simulate a long operation
        shared.mutex.unlock()


def version5(shared, tid):
    """This function implements another correct solution.

    The difference from version 4 is that the counter value is copied
    to a temporary variable which in this case allows us to minimize
    the critical area."""
    while True:
        shared.mutex.lock()
        tmp = shared.counter
        shared.counter += 1
        shared.mutex.unlock()
        if tmp >= shared.end:
            break
        print(f"Thread {tid} - counter: {tmp}")
        shared.arr[tmp] += 1
        sleep(1)  # Simulate a long operation


def main():
    """This function creates a shared object and multiple threads that access it."""
    num_threads = 3
    shared = Shared(5)
    threads = [Thread(version5, shared, i) for i in range(num_threads)]
    [t.join() for t in threads]
    print(shared.arr)


if __name__ == "__main__":
    main()
