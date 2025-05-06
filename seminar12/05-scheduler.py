"""Generator scheduler.

Skeletonized from Richard Korosi.
"""

from typing import Callable
from collections.abc import Generator


def consumer(func: Callable) -> Callable:
    """Call `next` automatically on a generator.

    Source: https://peps.python.org/pep-0342/"""

    def wrapper(*args, **kw):
        it = func(*args, **kw)
        next(it)
        return it

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


class Scheduler:
    """Scheduler for generator coprograms."""

    def __init__(self):
        """Initialize the scheduler."""
        self.jobs = []

    def add_job(self, it: Generator):
        """Add coprogram to the scheduler.

        :param it: coroutine to be added
        """

    def resume(self, rounds: int):
        """Start the scheduler.

        :param rounds: how many rounds of round-robin to run
        """


@consumer
def one():
    pass


@consumer
def two():
    pass


@consumer
def three():
    pass


def main():
    """Create and start the scheduler."""


if __name__ == "__main__":
    main()
