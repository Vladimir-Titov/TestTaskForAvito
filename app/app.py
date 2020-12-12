from typing import List, Callable
from typing import Optional

import asyncpg
from aiohttp import web
from aiohttp.web_routedef import RouteDef
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.update import update


class App(web.Application):
    pool: Optional[asyncpg.pool.Pool] = None
    scheduler: AsyncIOScheduler = AsyncIOScheduler()

    def __init__(self, routes: List[RouteDef], middlewares: List[Callable]):
        super().__init__(middlewares=middlewares)
        self.routes = routes

    async def _on_start(self, *args) -> None:
        self.pool = await asyncpg.create_pool(dsn="postgres://postgres:postgres@db/avitotask")
        self.scheduler.start()

    async def _on_stop(self, *args) -> None:
        await self.pool.close()
        self.scheduler.shutdown()

    def create_server(self, *args) -> None:
        """ Method for create server with init database
            and start scheduler """

        self.add_routes(self.routes)
        self.scheduler.add_job(update, 'interval', hours=1)
        self.on_startup.append(self._on_start)
        self.on_cleanup.append(self._on_stop)
