import asyncio


async def network_request(number):
    await asyncio.sleep(1.0)
    return {'success': True, "result": number ** 2}


async def fetch_square(number):
    response = await network_request(number)
    if response["success"]:
        print("result is: {}".format(response["result"]))

loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_square(2))
loop.run_until_complete(fetch_square(4))
