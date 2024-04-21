class MyIterator:
    def __init__(self, xs):
        self.xs = xs

    def __iter__(self):
        return self

    def __next__(self):
        if self.xs:
            return self.xs.pop(0)
        raise StopIteration


it = MyIterator([3, 4, 5])

print(it)

print(next(it))
print(next(it))
print(next(it))
print(next(it))
