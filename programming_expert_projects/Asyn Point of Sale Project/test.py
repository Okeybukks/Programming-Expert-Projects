import asyncio

urls = ['www.google.com', 'www.youtube.com', 'www.aol.com']

async def main():

    results = await asyncio.gather(map(fetch, urls))

asyncio.run(main())