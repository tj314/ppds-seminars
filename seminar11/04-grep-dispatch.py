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


@consumer
def dispatch(
    greps: Iterable[Generator[None, str, None]]
) -> Generator[None, str, None]:
    try:
        while True:
            line = yield
            for g in greps:
                g.send(line)
    except GeneratorExit:
        for g in greps:
            g.close()


def main():
    if len(sys.argv) < 3:
        print('usage: grep.py string... file', file=sys.stderr)
        sys.exit(-1)
    _file = open(sys.argv[-1])
    substrings = sys.argv[1:-1]
    greps = []

    for substring in substrings:
        c = count(substring)
        g = grep(substring, c)
        greps.append(g)

    d = dispatch(greps)
    cat(_file, d)


if __name__ == '__main__':
    main()
