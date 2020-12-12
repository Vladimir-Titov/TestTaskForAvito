from datetime import datetime

from aiohttp import web
from asyncpg import Record


class Views:

    def __init__(self, request: web.Request):
        self.request = request

    async def insert_query(self, query: str, region: str) -> Record:
        """
        Insert in DB a bunch of query and region and return Record object created id
        :param query: str
        :param region: str
        :return: object of Record class
        """
        async with self.request.app.pool.acquire() as connection:
            return await connection.fetchrow('''INSERT INTO query(query, region)
                                  VALUES ($1, $2)
                                  RETURNING id''', query, region)

    async def insert(self, count: int, query_id: int, top_5: list) -> Record:
        """
        Insert in DB count and timestamp
        :param top_5: list of the links
        :param count: int
        :param query_id: int
        :return: Record object
        """
        async with self.request.app.pool.acquire() as connection:
            await connection.fetchrow('''INSERT INTO top_5(query_id, links) 
                                         VALUES ($1, $2);''', query_id, top_5)
            return await connection.fetchrow('''INSERT INTO count_in_interval(count_items, query_id)  
                                                VALUES ($1, $2) 
                                                RETURNING id;''', count, query_id)

    async def for_update(self) -> None:
        """
        For update function
        :return: None
        """
        async with self.request.app.pool.acquire() as connection:
            return await connection.fetch('''SELECT id, query, region 
                                             FROM query ;''')

    async def track_count(self, id: int, start: datetime, end: datetime) -> Record:
        """

        return list of record object (count_items, time_stamp) between start and end
        :param id: int
        :param start: datetime in format %Y-%m-%d %H:%M
        :param end: datetime in format %Y-%m-%d %H:%M
        :return:
        """
        async with self.request.app.pool.acquire() as connection:
            return await connection.fetch('''SELECT count_items, time_stamp 
                                             FROM count_in_interval WHERE query_id=$1 and 
                                             time_stamp >= $2 and time_stamp <= $3;''', int(id), start, end)

    async def top_5(self, id: int) -> Record:
        """

        :param id: int
        :return: list link
        """

        async with self.request.app.pool.acquire() as connection:
            return await connection.fetch('''SELECT links FROM top_5 WHERE query_id=$1;''', int(id))
