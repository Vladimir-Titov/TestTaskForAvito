from aiohttp import web

from app.parse import parse
from app.schema import QueryString, ForStat
from app.views import Views


class Handler:
    """Class with app handler's"""

    def __init__(self):
        pass

    @staticmethod
    async def add(request: web.Request) -> web.json_response:
        """
        in request need querystring
        /add?query=$1&region=$2
        $1: str
        $2: str
        return record id of the created request object
        :param request: web.Request
        :return: web.json_response
        """
        data = dict(request.query)
        cleaned_data = QueryString().load(data)
        data['count_items'], top_5_link = await parse(**cleaned_data)
        id_create = await Views(request).insert_query(**cleaned_data)
        await Views(request).insert(count=data['count_items'], query_id=id_create[0], top_5=top_5_link)
        return web.json_response({'id': f'{id_create[0]}'})

    @staticmethod
    async def stat(request: web.Request) -> web.json_response:
        """
        in request need querystring
        /stat?id=$1&start=$2&end=$3
        $1: integer
        $2 and $3: datetime in format %Y-%m-%d %H:%M
        return list of time_stamps and count_items
        :param request: web.Request
        :return: web.json_response
        """

        data = dict(request.query)
        cleaned_data = ForStat().load(data)
        result = await Views(request).track_count(**cleaned_data)
        result_response = QueryString().dump(result, many=True)
        return web.json_response(data=result_response)

    @staticmethod
    async def update_count(request: web.Request) -> web.json_response:
        """

        Method for updating the quantity.
        Using only the update function
        :param request: web.Request
        :return: web.json_response
        """
        update_record = await Views(request).for_update()
        for elem in update_record:
            await Views(request).insert_count(count=await parse_count(elem[1], elem[2]), query_id=elem[0])
        return web.json_response({'update': 'success'})

    @staticmethod
    async def top_5(request: web.Request) -> web.json_response:
        """
        in request need querystring
        /top5?id=$1
        $1 : integer
        :param request: web.Request
        :return: web.json_response
        """
        data = dict(request.query)
        cleaned_data = QueryString(only=('id',)).load(data)
        result = await Views(request).top_5(**cleaned_data)
        result_response = QueryString(only=('links',)).dump(result, many=True)
        return web.json_response(data=result_response)
