# Source: https://realpython.com/async-io-python/

import random
import time


def makerandom(idx: int, threshold: int = 6) -> int:
    print(f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(f"makerandom({idx}) == {i} too low; retrying.")
        time.sleep(idx + 1)
        i = random.randint(0, 10)
    print(f"---> Finished: makerandom({idx}) == {i}")
    return i


def main():
    for i in range(3):
        makerandom(i, 10 - i - 1)


random.seed(444)
main()
