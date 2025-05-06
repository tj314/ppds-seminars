from random import randint


def generator(n: int):
    """Pretend to read something from I/O `n` times."""
    while n:
        n -= 1
        msg = yield f'read {n}: {randint(1, 1000)}'
        print(f'generator received {msg}')
    return 'End'


def connector(gen):
    """Transparently connect another generator `gen`."""
    n = 0
    while n < 3:
        n += 1
        msg = yield f'This is connector, msg. n. {n}'
        print(f'connector received {msg}')
        msg = yield from gen
        print(f'connector received from gen {msg}')


it = connector(generator(3))
first_msg = next(it)
print(f'first message is {first_msg}')
n = 100
try:
    while True:
        received = it.send(n)
        print(f'main received {received}')
        n += 10
except StopIteration:
    pass
