from typing import Callable


def consumer(func: Callable) -> Callable:
    def wrapper(*args, **kw):
        it = func(*args, **kw)
        next(it)
        return it

    wrapper.__name__ = func.__name__
    wrapper.__dict__ = func.__dict__
    wrapper.__doc__ = func.__doc__
    return wrapper


@consumer
def complain_about(substring: str):
    print('Please talk to me!')
    try:
        while True:
            text = yield
            if substring in text:
                print(f'Oh no: I found a {substring} again!')
    except GeneratorExit:
        print('Ok, ok: I am quitting.')


it = complain_about('JavaScript')

it.send('Test data with JavaScript somewhere in it')
it.close()
