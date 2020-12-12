from typing import Callable

from aiohttp import web
from aiohttp.client_exceptions import ClientConnectionError
from marshmallow.exceptions import ValidationError


@web.middleware
async def error_middleware(request: web.Request,
                           handler: Callable[[web.Request], web.json_response]) -> web.json_response:
    """
    Middleware for interception any exception:
    :param request: web.Request
    :param handler: Callable[[web.Request], web.json_response])
    :return: web.json_response
    """

    try:
        return await handler(request)
    except (ValidationError, AttributeError, ClientConnectionError) as ex:
        return web.json_response({'error': f'{ex}'})
