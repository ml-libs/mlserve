import asyncio
import json
import os

import trafaret as t
import yaml

from aiohttp import web
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, List, Dict

from .handlers import (
    APIHandler,
    SiteHandler,
    setup_app_routes,
    setup_api_routes,
)
from .worker import warm
from .middleware import stats_middleware


PROJ_ROOT = Path(__file__).parent.parent

ModelMeta = t.Dict(
    {
        t.Key('name'): t.String,
        t.Key('description'): t.String,
        t.Key('model_path'): t.String,
        t.Key('data_schema_path'): t.String,
        t.Key('target'): t.String,
    }
)

ModelConfig = t.Dict({t.Key('models'): t.List(ModelMeta)})


def load_model_config(fname):
    with open(fname, 'rt') as f:
        raw_data = yaml.safe_load(f)
    data = ModelConfig(raw_data)
    return data


async def setup_executor(app, max_workers, models):
    executor = ProcessPoolExecutor(max_workers=max_workers)
    loop = asyncio.get_event_loop()
    run = loop.run_in_executor
    fs = [run(executor, warm, models) for i in range(0, max_workers)]
    await asyncio.gather(*fs)

    async def close_executor(app):
        # TODO: figureout timeout for shutdown
        executor.shutdown(wait=True)

    app.on_cleanup.append(close_executor)
    app['executor'] = executor
    return executor


@dataclass
class ModelDescriptor:
    name: str
    target: str
    features: List[str]
    schema: Dict[Any, Any]
    model_path: Path
    model_size: int
    data_schema_path: Path
    schema_size: int

    def asdict(self):
        return asdict(self)


def get_executor(request):
    executor = request.app['executor']
    return executor


def load_models(model_conf):
    result = []
    for m in model_conf:
        with open(m['data_schema_path'], 'rb') as f:
            schema = json.load(f)

        schema_size = os.path.getsize(m['data_schema_path'])
        model_size = os.path.getsize(m['model_path'])
        features = list(schema['properties'].keys())
        model_desc = ModelDescriptor(
            name=m['name'],
            target=m['target'],
            features=features,
            schema=schema,
            model_path=m['model_path'],
            model_size=model_size,
            data_schema_path=m['data_schema_path'],
            schema_size=schema_size,
        )
        result.append(model_desc)
    return result


async def init(loop, max_workers, model_conf) -> web.Application:
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
