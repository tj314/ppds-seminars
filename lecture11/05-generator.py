def generator(n):
    while n:
        n -= 1
        yield n


for i in generator(3):
    print(i)
