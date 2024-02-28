"""This module implements the LightSwitch data type."""

__author__ = "Tomáš Vavro"
__email__ = "tomas.vavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Semaphore


class LightSwitch:
    """This class implements the LightSwitch data type."""
    def __init__(self):
        """Initialize the LightSwitch object."""
        self.counter = 0
        self.mutex = Semaphore(1)

    def lock(self, semaphore):
        """Lock the LightSwitch."""
        self.mutex.wait()
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.signal()

    def unlock(self, semaphore):
        """Unlock the LightSwitch."""
        self.mutex.wait()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.signal()
