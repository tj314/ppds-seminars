# Source: https://realpython.com/python-async-features/

import queue


def task(name, work_queue):
    while not work_queue.empty():
        count = work_queue.get()
        total = 0
        print(f'Task {name} running')
        for i in range(count):
            total += 1
            yield
        print(f'Task {name} total: {total}')


def main():
    work_queue = queue.Queue()

    for work in [17, 9, 10, 5]:
        work_queue.put(work)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
    ]

    done = False
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if not tasks:
                done = True


if __name__ == '__main__':
    main()
