from aiohttp import web

from app.handler import Handler

routes = [web.get('/add', Handler.add),
          web.get('/stat', Handler.stat),
          web.get('/update', Handler.update_count),
          web.get('/top5', Handler.top_5)
          ]
