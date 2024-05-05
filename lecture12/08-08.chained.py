# Source: https://realpython.com/async-io-python/

import asyncio
import random
import time


async def part1(n: int) -> str:
    i = random.randint(0, 10)
    print(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"--> res{n}-1"
    print(f"Returning part1({n}) == '{result}'.")
    return result


async def part2(n: int, arg: str) -> str:
    i = random.randint(0, 10)
    print(f"part2{n, arg} sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f"{arg} --> res{n}-2"
    print(f"Returning part2{n, arg} == '{result}'.")
    return result


async def chain(n: int) -> None:
    p1 = await part1(n)
    p2 = await part2(n, p1)
    print(f"*** Chained res{n} => '{p2}'.")


async def main(*args):
    await asyncio.gather(*(chain(n) for n in args))


random.seed(444)
asyncio.run(main(1, 2, 3))
print(f"Program finished.")
