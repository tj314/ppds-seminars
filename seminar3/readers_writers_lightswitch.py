"""This module implements a solution to the readers writers problem using the LightSwitch data type."""

__author__ = "Tomáš Vavro"
__email__ = "tomas.vavro@stuba.sk"
__license__ = "MIT"


from lightswitch import LightSwitch
from fei.ppds import Thread, Semaphore, print
from time import sleep


class Shared:
    """This class contains the shared data and the synchronization objects."""
    def __init__(self):
        self.ls = LightSwitch()
        self.lock = Semaphore(1)
        self.turnstile = Semaphore(1)


def reader(shared, tid):
    """This function represents the reader's behavior.

    :param shared: an instance of the Shared class
    :param tid: thread id
    """
    while True:
        shared.turnstile.wait()
        shared.ls.lock(shared.lock)
        shared.turnstile.signal()

        print(f"Reader {tid} is reading.")
        sleep(0.1)
        shared.ls.unlock(shared.lock)
        print(f"Reader {tid} finished reading.")
        sleep(0.2)  # simulate the time between two consecutive readings


def writer(shared, tid):
    """This function represents the writer's behavior.

    :param shared: an instance of the Shared class
    :param tid: thread id
    """
    while True:
        shared.turnstile.wait()
        shared.lock.wait()
        print(f"Writer {tid} is writing.")
        sleep(0.2)
        shared.lock.signal()
        shared.turnstile.signal()
        print(f"Writer {tid} finished writing.")
        sleep(0.5)  # simulate the time between two consecutive writings


def main():
    """This function represents the entry point of the program.

    It creates the shared data and the threads for readers and writers.
    """
    num_readers = 5
    num_writers = 10
    shared = Shared()
    threads = [Thread(reader, shared, i) for i in range(num_readers)] +\
              [Thread(writer, shared, i) for i in range(num_writers)]
    [t.join() for t in threads]


if __name__ == "__main__":
    main()
