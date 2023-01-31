import asyncio
import time
import requests
import aiohttp


async def get_url_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def async_sleep(n):
    print('Before sleep', n)
    n = max(2, n)
    for i in range(1, n):
        yield i
        await asyncio.sleep(i)
    print('after sleep', n)


async def print_hello():
    print('Hello')


async def main():

    urls = [
        'https://google.com',
        'https://apple.com',
        'https://python.org',
        'https://medium.com'
    ]
    start = time.time()
    sync_text_response = []
    for url in urls:
        sync_text_response.append(requests.get(url=url).text)
    print('sync total time: ', time.time() - start)

    start = time.time()
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_url_response(url)))

    async_text_response = await asyncio.gather(*tasks)

    print('async request total time: ', time.time() - start)


if __name__ == '__main__':
    asyncio.run(main())
