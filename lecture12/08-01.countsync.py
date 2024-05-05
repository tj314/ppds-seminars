# Source: https://realpython.com/async-io-python/

import time


def count():
    print("One")
    time.sleep(1)
    print("Two")


def main():
    for _ in range(3):
        count()


s = time.perf_counter()
main()
elapsed = time.perf_counter() - s
print(f"program executed in {elapsed:0.2f} seconds.")
