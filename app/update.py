import aiohttp


async def update() -> None:
    """
    Function called only scheduler
    :return: None
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8080/update') as resp:
            return None
