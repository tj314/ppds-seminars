"""This module implements a combining tree barrier.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Tomáš Vavro"
__email__ = "tomas.vavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Semaphore, print
import math


class CombiningTreeBarrier:
    """Implements a combining tree barrier."""
    def __init__(self, num_threads):
        """Initializes the barrier with the number of threads."""
        if not math.log(num_threads + 1, 2).is_integer():
            print(f"Number threads N must be 2^k - 1")
            raise ValueError
        self.num_threads = num_threads
        self.in_semaphores = [Semaphore(0) for _ in range(num_threads)]
        self.out_semaphores = [Semaphore(0) for _ in range(num_threads)]

    @staticmethod
    def get_children(tid):
        """Returns the ids of the children of a node."""
        return 2*tid + 1, 2*tid + 2

    @staticmethod
    def is_leaf(tid, num_threads):
        """Returns True if the node is a leaf node."""
        return 2*tid + 1 >= num_threads

    def wait(self, tid):
        """Waits for all threads to arrive at the barrier."""
        if CombiningTreeBarrier.is_leaf(tid, self.num_threads):  # leaf node
            self.in_semaphores[tid].signal()
            self.out_semaphores[tid].wait()
        elif tid == 0:  # root node
            left_child, right_child = CombiningTreeBarrier.get_children(tid)
            self.in_semaphores[left_child].wait()
            self.in_semaphores[right_child].wait()
            self.out_semaphores[left_child].signal()
            self.out_semaphores[right_child].signal()
        else:  # in between node
            left_child, right_child = CombiningTreeBarrier.get_children(tid)
            self.in_semaphores[left_child].wait()
            self.in_semaphores[right_child].wait()
            self.in_semaphores[tid].signal()
            self.out_semaphores[tid].wait()
            self.out_semaphores[left_child].signal()
            self.out_semaphores[right_child].signal()


class Shared:
    """Represents shared data."""
    def __init__(self, num_threads):
        """Initializes the shared data."""
        self.num_threads = num_threads
        self.barrier = CombiningTreeBarrier(num_threads)


def worker(shared, tid):
    """Represents a worker thread."""
    print(f"Thread {tid} has arrived to the barrier.")
    shared.barrier.wait(tid)
    print(f"Thread {tid} has passed the barrier.")


def main():
    """Main function."""
    num_threads = 7
    sh = Shared(num_threads)
    threads = [Thread(worker, sh, i) for i in range(num_threads)]
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
