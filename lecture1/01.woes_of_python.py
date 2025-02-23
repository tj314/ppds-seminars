"""Example of Python programming."""

__authors__ = "Matúš Jókay, Roderik Ploszek"
__license__ = "MIT"

import fei.ppds


def mocnina(m, n=3):
    """Compute m to the power of n."""
    return m**n


class Shared:
    """Example class that wraps an internal value."""

    def __init__(self):
        """Initialize internal value to 3."""
        self.m = 3

    def print_m(self):
        """Print internal value."""
        print(self.m)

    def get_m(self):
        """Return internal value."""
        return m


print(mocnina(2, 5))
s = Shared()
s.print_m()

s = fei.ppds.Semaphore(1)
print(s.value())

m = fei.ppds.Mutex()
m.lock()
# KO
m.unlock()
