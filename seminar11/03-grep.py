import sys
from collections.abc import Generator, Iterable
from typing import TextIO, Callable


def consumer(func: Callable) -> Callable:
    def wrapper(*args, **kw):
        it = func(*args, **kw)
        next(it)
        return it

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


def cat(_file: TextIO, gen: Generator[None, str, None]):
    for line in _file:
        gen.send(line)
    gen.close()


@consumer
def grep(
    substring: str, gen: Generator[None, int, None]
) -> Generator[None, str, None]:
    try:
        while True:
            line = yield
            gen.send(line.count(substring))
    except GeneratorExit:
        gen.close()


@consumer
def count(substring: str) -> Generator[None, int, None]:
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
