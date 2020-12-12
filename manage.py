import logging
from app.middlewares import error_middleware
from aiohttp import web

from app import App
from app.routes import routes

if __name__ == '__main__':
    app = App(routes, middlewares=[error_middleware])
    app.create_server()
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)
