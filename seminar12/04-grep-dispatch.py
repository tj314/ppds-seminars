import sys
from collections.abc import Generator, Iterable
from typing import TextIO, Callable


def consumer(func: Callable) -> Callable:
    """Call `next` automatically on a generator."""

    def wrapper(*args, **kw):
        it = func(*args, **kw)
        next(it)
        return it

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


def cat(file_: TextIO, gen: Generator[None, str, None]):
    """Read file line after line.

    :param file_: file object from which to read.
    :param gen: coroutine to which the line will be sent.
    """
    for line in file_:
        gen.send(line)
    return gen.close()


@consumer
def grep(
    substring: str, gen: Generator[None, int, None]
) -> Generator[None, str, None]:
    """Count number of occurences of a string `substring`.

    :param gen: coroutine to which the number of occurences will be
    sent.
    """
    try:
        while True:
            line = yield
            gen.send(line.count(substring))
    except GeneratorExit:
        return gen.close()


@consumer
def count(substring: str) -> Generator[None, int, None]:
    """Count number of occurences of a string `substring`.

    :param gen: coroutine to which the number of occurences will be
    sent.
    """
    n = 0
    try:
        while True:
            n += yield
    except GeneratorExit:
        return substring, n


@consumer
def dispatch(
    greps: Iterable[Generator[None, str, None]],
) -> Generator[None, str, None]:
    """Sum received values.

    The result will be printed on the screen after this coroutine is
    closed.
    """
    try:
        while True:
            line = yield
            for g in greps:
                g.send(line)
    except GeneratorExit:
        return [g.close() for g in greps]


def main():
    if len(sys.argv) < 3:
        print('usage: grep.py string... file', file=sys.stderr)
        sys.exit(-1)
    file_ = open(sys.argv[-1])
    substrings = sys.argv[1:-1]
    greps = []

    for substring in substrings:
        c = count(substring)
        g = grep(substring, c)
        greps.append(g)

    d = dispatch(greps)
    print(cat(file_, d))


if __name__ == '__main__':
    main()
