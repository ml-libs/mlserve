import asyncio

from aiohttp import web
from concurrent.futures import ProcessPoolExecutor
from typing import Any, List, Dict

from .handlers import (
    APIHandler,
    SiteHandler,
    setup_app_routes,
    setup_api_routes,
)
from .consts import PROJ_ROOT
from .middleware import stats_middleware
from .utils import ModelDescriptor, load_models
from .worker import warm


async def setup_executor(
    app: web.Application,
    max_workers: int,
    models: List[ModelDescriptor]
) -> ProcessPoolExecutor:
    executor = ProcessPoolExecutor(max_workers=max_workers)
    loop = asyncio.get_event_loop()
    run = loop.run_in_executor
    fs = [run(executor, warm, models) for i in range(0, max_workers)]
    await asyncio.gather(*fs)

    async def close_executor(app: web.Application) -> None:
        # TODO: figureout timeout for shutdown
        executor.shutdown(wait=True)

    app.on_cleanup.append(close_executor)
    app['executor'] = executor
    return executor


async def init(
    max_workers: int, model_conf: Dict[str, Any]
) -> web.Application:
    # setup web page related routes
    app = web.Application()
    handler = SiteHandler(PROJ_ROOT)
    setup_app_routes(app, handler)

    # setup API routes
    api = web.Application(middlewares=[stats_middleware])
    models = load_models(model_conf['models'])
    executor = await setup_executor(app, max_workers, models)
    api_handler = APIHandler(api, executor, PROJ_ROOT, models)
    setup_api_routes(api, api_handler)

    app.add_subapp('/api', api)
    return app
