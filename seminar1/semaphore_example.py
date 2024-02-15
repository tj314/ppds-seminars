"""This module implements semaphore examples from the seminar 1."""

__authors__ = "Marián Šebeňa, Tomáš Vavro"
__license__ = "MIT"

from fei.ppds import Thread, Semaphore, print
from time import sleep
from random import randint


class Shared:
    """This class represents shared data."""
    def __init__(self, semaphore):
        """Initializes shared data."""
        self.semaphore = semaphore


def crossroads(shared, tid):
    """This function simulates a deeply philosophical and metaphysical question.

    The question is: "Which road should I take?" To some extent,
    it is similar to the question of whether to lock a mutex or not.
    Considering the general nature of a semaphore, it is, without a doubt,
    a better suited way to answer such profound questions.
    More precisely, this problem is a perfect foray into the epistemology
    (and consequently ontology) of oneself.
    """
    for _ in range(3):
        shared.semaphore.wait()
        print(f"Thread {tid} is on the crossroads.")
        sleep(randint(1,5)/10)  # simulates a long reflexion of which road to take
        print(f"Thread {tid} has passed the crossroads.")
        shared.semaphore.signal()


def main1():
    """This function demonstrates the use of a semaphore.

    More specifically, it demonstrates the case in which
    the semaphore is initialized to a higher value than number of created threads.
    Notice that all threads all allowed to enter the critical area at the same time.
    """
    n_threads = 2
    semaphore = Semaphore(3)
    shared = Shared(semaphore)
    threads = [Thread(crossroads, shared, i) for i in range(n_threads)]
    [t.join() for t in threads]


def main2():
    """This function demonstrates the use of a semaphore.

    More specifically, it demonstrates the case in which
    the semaphore is initialized to a lower value than number of created threads.
    Notice that only the first three threads are allowed to enter the critical area at the same time.
    """
    n_threads = 5
    semaphore = Semaphore(3)
    shared = Shared(semaphore)
    threads = [Thread(crossroads, shared, i) for i in range(n_threads)]
    [t.join() for t in threads]


def main3():
    """This function demonstrates the use of a semaphore.

    More specifically, it demonstrates the case in which
    the semaphore is initialized to 0.
    Notice that none of the threads are allowed to enter the critical area,
    which results in a deadlock.
    """
    n_threads = 5
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    threads = [Thread(crossroads, shared, i) for i in range(n_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main1()
    # main2()
    # main3()
