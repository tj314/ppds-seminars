# Source: https://realpython.com/async-io-python/

import asyncio
import time


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def main():
    await asyncio.gather(count(), count(), count())


s = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - s
print(f"program executed in {elapsed:0.2f} seconds.")
