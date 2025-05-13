# Source: https://realpython.com/python-async-features/

import queue


def task(name, work_queue):
    if work_queue.empty():
        print(f'Task {name} nothing to do')
        return
    while not work_queue.empty():
        count = work_queue.get()
        total = 0
        print(f'Task {name} running')
        for i in range(count):
            total += 1
        print(f'Task {name} total: {total}')


def main():
    work_queue = queue.Queue()

    # Prepare work queue with objects to be processed
    for work in [17, 9, 10, 5]:
        work_queue.put(work)

    # Prepare tasks
    tasks = (
        (task, 'One', work_queue),
        (task, 'Two', work_queue),
    )

    # Start tasks
    for f, n, q in tasks:
        f(n, q)


if __name__ == '__main__':
    main()
