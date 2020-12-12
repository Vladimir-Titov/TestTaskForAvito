from typing import Optional

import asyncpg
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import dsn
from update import update


class App(web.Application):
    poll: Optional[asyncpg.pool.Pool] = None
    scheduler: AsyncIOScheduler = AsyncIOScheduler()

    def __init__(self, routes, middlewares):
        super().__init__(middlewares=middlewares)
        self.routes = routes

    async def _on_start(self, *args) -> None:
        self.poll = await asyncpg.create_pool(dsn=dsn)
        self.scheduler.start()

    async def _on_stop(self, *args) -> None:
        await self.poll.close()
        self.scheduler.shutdown()

    def create_server(self, *args) -> None:
        self.add_routes(self.routes)
        self.scheduler.add_job(update, 'interval', hours=1)
        self.on_startup.append(self._on_start)
        self.on_cleanup.append(self._on_stop)
