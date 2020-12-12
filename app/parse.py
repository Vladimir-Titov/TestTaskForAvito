import aiohttp
from bs4 import BeautifulSoup

from settings import headers


async def parse_count(query: str, region: str) -> int:
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://www.avito.ru/{region}?q={query}') as resp:
            page = await resp.text()
    soup = BeautifulSoup(page, 'html.parser')
    count = soup.find('span', class_="page-title-count-1oJOc")
    return int(''.join(count.contents[0].split()))
