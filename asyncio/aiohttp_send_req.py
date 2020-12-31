#!/usr/bin/env python3
#encoding:utf-8 
# areq.py

import sys
import time
import aiohttp
import asyncio
from aiohttp import ClientSession

async def put_pcapng(url,session,semaphore,data,headers):
    async with semaphore:
        async with session.put(url,data=data,headers=headers) as resp:
            if resp.status == 200:
                return await resp.read()
            else:
                print(f"ERROR: {time.strftime('%X')} {resp.status} {url}.")


async def main(urls, data, headers):
    #设置最大并发量
    semaphore =asyncio.Semaphore(500)
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                put_pcapng(url=url, session=session, semaphore=semaphore,data=data,headers=headers)
            )
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."

    with open('test.pcapng', 'rb') as f:
        data = f.read()

    headers = {
            "Content-Type":"pcapng",
            "token":"xxxxxxxxxxxxxxxxxxxxxxxx"
    }

    u = 'http://endpoint_url/<bucket_name>/<key>'

    urls = []
    for i in range(1,4001):
        url = u + 'test' + str(i) + '.pcapng'
        urls.append(url)  

    print(f"started at {time.strftime('%X')}")
    asyncio.run(main(urls,data,headers))
    print(f"finished at {time.strftime('%X')}")
    



