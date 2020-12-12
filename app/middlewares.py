from aiohttp import web
from aiohttp.client_exceptions import ClientConnectionError
from marshmallow.exceptions import ValidationError


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except (ValidationError, AttributeError, ClientConnectionError) as ex:
        return web.json_response({'error': f'{ex}'})
