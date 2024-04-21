class MyIterator:
    def __init__(self, xs):
        self.xs = xs

    def __iter__(self):
        return self

    def __next__(self):
        if self.xs:
            return self.xs.pop(0)
        raise StopIteration


for i in MyIterator([0, 1, 2]):
    print(i)
