"""Simple timer."""

__authors__ = "Roderik Ploszek"
__license__ = "GPL-3.0-or-later"

from time import perf_counter_ns


TIMER = perf_counter_ns


class Timer:
    """Simple timer.

    Uses perf_counter_ns by default.
    """
    def __init__(self):
        """Start the timer."""
        self.lap = TIMER()

    def reset(self):
        """Reset the timer to zero and start it again."""
        self.lap = TIMER()

    def lap_ms(self):
        """Check the current value of the timer.

        :returns: Current number of ms after the last start of the
        timer.
        """
        old_lap = self.lap
        lap = TIMER()
        return (lap - old_lap) / 1_000_000
