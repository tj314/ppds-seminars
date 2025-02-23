"""Example of nondeterministic behavior."""

__authors__ = "Matúš Jókay, Roderik Ploszek"
__license__ = "MIT"

from time import sleep
from random import randint as rand
from fei.ppds import Thread


def fnc_yes():
    """Print yes in a loop with some random sleep."""
    while True:
        sleep(rand(1, 10) / 12)
        print('yes')


def fnc_no():
    """Print no in a loop with some random sleep."""
    while True:
        sleep(rand(1, 10) / 12)
        print('no')


threads = [Thread(fnc_yes), Thread(fnc_no)]

for t in threads:
    t.join()
