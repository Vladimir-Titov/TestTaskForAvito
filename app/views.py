from datetime import datetime

from aiohttp import web


class Views:

    def __init__(self, request: web.Request):
        self.request = request

    async def insert_query(self, query: str, region: str):
        async with self.request.app.poll.acquire() as connection:
            return await connection.fetchrow('''INSERT INTO query(query, region)
                                  VALUES ($1, $2)
                                  RETURNING id''', query, region)

    async def insert_count(self, count: int, query_id: int):
        async with self.request.app.poll.acquire() as connection:
            return await connection.fetchrow('''INSERT INTO count_in_interval(count_items, query_id)  
                                                VALUES ($1, $2) 
                                                RETURNING id''', count, query_id)

    async def for_update(self):
        async with self.request.app.poll.acquire() as connection:
            return await connection.fetch('''SELECT id, query, region 
                                             FROM query ''')

    async def track_count(self, id: int, start: datetime, end: datetime):
        async with self.request.app.poll.acquire() as connection:
            return await connection.fetch('''SELECT count_items, time_stamp 
                                             FROM count_in_interval WHERE query_id=$1 and 
                                             time_stamp >= $2 and time_stamp <= $3''', int(id), start, end)
