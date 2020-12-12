from aiohttp import web

from handler import Handler

routes = [web.get('/add', Handler.add),
          web.get('/stat', Handler.stat),
          web.get('/update', Handler.update_count)
          ]
