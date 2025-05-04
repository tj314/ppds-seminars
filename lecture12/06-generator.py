def generator(n):
    while n:
        n -= 1
        yield n


it = generator(3)

print(generator)
print(it)

print(next(it))
print(next(it))
print(next(it))
