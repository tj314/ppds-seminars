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
    gen.close()


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
        gen.close()


@consumer
def count(substring: str) -> Generator[None, int, None]:
    """Sum received values.

    The result will be printed on the screen after this coroutine is
    closed.
    """
    n = 0
    try:
        while True:
            n += yield
    except GeneratorExit:
        print(substring, n)


def main():
    if len(sys.argv) < 3:
        print('usage: grep.py string... file', file=sys.stderr)
        sys.exit(-1)
    file = open(sys.argv[-1])
    substring = sys.argv[1]

    c = count(substring)
    g = grep(substring, c)

    cat(file, g)


if __name__ == '__main__':
    main()
