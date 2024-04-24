class Fibonacci:
    """Generate Fibonacci sequence."""
    def __init__(self, limit: int):
        self.a = 0
        self.b = 1
        self.i = 1
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.i > self.limit:
            raise StopIteration

        if self.i > 1:
            self.a, self.b = self.b, self.a + self.b

        self.i += 1
        return self.b
