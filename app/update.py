import aiohttp


async def update():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/update') as resp:
            return resp.status
