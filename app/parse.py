from typing import List, Tuple

import aiohttp
from bs4 import BeautifulSoup

from settings import headers


async def parse(query: str, region: str) -> Tuple[int, list]:
    """
    Parse avito.ru and return count_items in the querystring
    :param query: str
    :param region: str
    :return: int
    """
    top_5 = []
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://www.avito.ru/{region}?q={query}') as resp:
            page = await resp.text()
    soup = BeautifulSoup(page, 'html.parser')
    count = soup.find('span', class_="page-title-count-1oJOc")
    all_link = soup.find_all('a',
                             class_="link-link-39EVK link-design-default-2sPEv title-root-395AQ iva-item-title-1Rmmj title-list-1IIB_ title-root_maxHeight-3obWc")
    for index, link in enumerate(all_link):
        top_5.append(link.get('href'))
        if index == 4:
            break
    return int(''.join(count.contents[0].split())), top_5
