from collections.abc import Generator


def complain_about(substring: str):
    print('Please talk to me!')
    try:
        while True:
            text = yield
            if substring in text:
                print(f'Oh no: I found a {substring} again!')
    except GeneratorExit:
        print('Ok, ok: I am quitting.')
    except RuntimeError:
        print('Something funny happened.')
        yield 'I have handled the exception.'


it = complain_about('Ruby')

next(it)
it.send('ahoj Ruby')
print(it.throw(RuntimeError))
# it.send('ahoj svjete!')
# it.send('no znovu Ruby na riadku')
# it.close()

# it.send('toto nepojde')
# next(it)
