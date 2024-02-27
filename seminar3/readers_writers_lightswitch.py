"""This module implements a solution to the readers writers problem using the LightSwitch data type."""

__author__ = "Tomáš Vavro"
__email__ = "tomas.vavro@stuba.sk"
__license__ = "MIT"


from lightswitch import LightSwitch
from fei.ppds import Thread, Mutex, print
from time import sleep


class Shared:
    """This class contains the shared data and the synchronization objects."""
    def __init__(self):
        self.ls = LightSwitch()
        self.lock = Mutex()


def reader(shared, tid):
    """This function represents the reader's behavior.

    :param shared: an instance of the Shared class
    :param tid: thread id
    """
    while True:
        shared.ls.lock(shared.lock)
        print(f"Reader {tid} is reading.")
        sleep(0.1)
        shared.ls.unlock(shared.lock)


def writer(shared, tid):
    """This function represents the writer's behavior.

    :param shared: an instance of the Shared class
    :param tid: thread id
    """
    while True:
        shared.lock.lock()
        print(f"Writer {tid} is writing.")
        sleep(0.2)
        shared.lock.unlock()


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
