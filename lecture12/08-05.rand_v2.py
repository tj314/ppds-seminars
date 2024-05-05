# Source: https://realpython.com/async-io-python/

import random
import time
import asyncio


async def makerandom(idx: int, threshold: int = 6) -> int:
    print(f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(f"makerandom({idx}) == {i} too low; retrying.")
        time.sleep(idx + 1)
        i = random.randint(0, 10)
    print(f"---> Finished: makerandom({idx}) == {i}")
    return i


async def main():
    for i in range(3):
        await makerandom(i, 10 - i - 1)


random.seed(444)
t = time.time()
asyncio.run(main())
print(f"\nTime elapsed:{time.time()-t}")
