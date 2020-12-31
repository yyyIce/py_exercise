#!/usr/bin/env python3
# asynciotest3.py
import asyncio
import time

async def nested():
    print("Coro nested Started.")
    await asyncio.sleep(3)
    print("Coro nested Finished.")

async def main():
    print("Coro main Started.")
    #task = asyncio.create_task(nested())
    #await task
    await asyncio.gather(nested())
    print("Coro main Finished.")

if __name__ == "__main__":
    print(f"started at {time.strftime('%X')}")
    asyncio.run(main())
    print(f"finished at {time.strftime('%X')}")
