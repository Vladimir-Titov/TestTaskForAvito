from aiohttp import web

from parse import parse_count
from schema import QueryString, ForStat
from views import Views


class Handler:

    def __init__(self):
        pass

    @staticmethod
    async def add(request: web.Request) -> web.json_response:
        data = dict(request.query)
        cleaned_data = QueryString().load(data)
        data['count_items'] = await parse_count(**cleaned_data)
        id_create = await Views(request).insert_query(**cleaned_data)
        await Views(request).insert_count(count=data['count_items'], query_id=id_create[0])
        return web.json_response({'id': f'{id_create[0]}'})

    @staticmethod
    async def stat(request: web.Request) -> web.json_response:
        data = dict(request.query)
        cleaned_data = ForStat().load(data)
        result = await Views(request).track_count(**cleaned_data)
        result_response = QueryString().dump(result, many=True)
        return web.json_response(data=result_response)

    @staticmethod
    async def update_count(request: web.Request):
        update_record = await Views(request).for_update()
        for elem in update_record:
            await Views(request).insert_count(count=await parse_count(elem[1], elem[2]), query_id=elem[0])
        return web.json_response({'update': 'success'})
