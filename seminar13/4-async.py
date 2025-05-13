# Source: https://realpython.com/python-async-features/

import asyncio
import queue
import time


# TODO: Funkcie musia byt asynchronne.
#       Pouzite asynchronne volania, kde to je vhodne.

def task(name, work_queue):
    while not work_queue.empty():
        delay = work_queue.get()
        print(f'Task {name} running')
        time_start = time.perf_counter()
        time.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f'Task {name} elapsed time: {elapsed:.1f}')
        yield


def main():
    # TODO: Pouzite spravny front
    work_queue = queue.Queue()

    for work in [5, 3, 4, 1]:
        work_queue.put(work)

    time_start = time.perf_counter()

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
    ]

    # TODO: Vykonajte ulohy `tasks` asynchronne

    elapsed = time.perf_counter() - time_start
    print(f'\n Total elapsed time: {elapsed:.1f}')


if __name__ == '__main__':
    asyncio.run(main())
