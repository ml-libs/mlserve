import asyncio
import json

from aiohttp import web
from functools import partial
from pathlib import Path
from typing import Callable, Dict, Any, Union, List

from .consts import MODELS_KEY
from .exceptions import ObjectNotFound
from .stats import ModelStats, AggStats
from .worker import predict


def path_serializer(obj: Any) -> str:
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError('Type not serializable')


jsonify = partial(
    json.dumps, indent=4, sort_keys=True, default=path_serializer)
JsonResp = Callable[[Union[Dict[str, Any], List[Any]]], web.Response]
json_response: JsonResp = partial(web.json_response, dumps=jsonify)


class SiteHandler:
    def __init__(self, project_root: Path) -> None:
        self._root = project_root
        self._loop = asyncio.get_event_loop()

    @property
    def project_root(self) -> Path:
        return self._root

    async def index(self, request: web.Request) -> web.FileResponse:
        path = str(self._root / 'static' / 'index.html')
        return web.FileResponse(path)


def setup_app_routes(
    app: web.Application, handler: SiteHandler
) -> web.Application:
    r = app.router
    h = handler
    path = str(handler.project_root / 'static')
    r.add_get('/', h.index, name='index')
    r.add_get('/models', h.index, name='index.models')
    r.add_get('/models/{model_name}', h.index, name='index.model.name')
    r.add_static('/static/', path=path, name='static')
    return app


class APIHandler:

    def __init__(self, app: web.Application,
                 executor, project_root: Path, model_desc):
        self._app = app
        self._executor = executor
        self._root = project_root
        self._loop = asyncio.get_event_loop()

        self._models = {m.name: m for m in model_desc}
        self._app[MODELS_KEY] = {m.name: ModelStats() for m in model_desc}

        result = sorted(self._models.values(), key=lambda v: v.name)
        self._models_list = [
            {'name': m.name, 'target': m.target} for m in result
        ]

    def validate_model_name(self, model_name: str) -> str:
        if model_name not in self._models:
            msg = f'Model with name {model_name} not found.'
            raise ObjectNotFound(msg)
        return model_name

    async def model_list(self, request: web.Request) -> web.Response:
        return json_response(self._models_list)

    async def model_detail(self, request: web.Request):
        model_name = request.match_info['model_name']
        self.validate_model_name(model_name)

        r = self._models[model_name].asdict()
        return json_response(r)

    async def model_predict(self, request: web.Request) -> web.Response:
        model_name = request.match_info['model_name']
        self.validate_model_name(model_name)
        raw_data = await request.read()
        run = self._loop.run_in_executor
        # TODO: figure out if we need protect call with aiojobs
        r = await run(self._executor, predict, model_name, raw_data)
        # TODO: introduce exception in case of model failure to predict
        # msg = 'Model failed to predict'
        # raise UnprocessableEntity(msg, reason=str(e)) from e

        return json_response(r)

    async def model_stats(self, request: web.Request) -> web.Response:
        model_name = request.match_info['model_name']
        stats: ModelStats = request.app[MODELS_KEY][model_name]
        r = stats.formatted()
        return json_response(r)

    async def agg_stats(self, request: web.Request) -> web.Response:
        stats_map: Dict[str, ModelStats] = request.app[MODELS_KEY]
        agg = AggStats.from_models_stats(stats_map)
        return json_response(agg.formatted())


def setup_api_routes(
    api: web.Application, handler: APIHandler
) -> web.Application:
    r = api.router
    h = handler
    r.add_get('/v1/agg_stats', h.agg_stats, name='stats.list')
    r.add_get('/v1/models', h.model_list, name='models.list')
    r.add_get('/v1/models/{model_name}', h.model_detail, name='models.detail')
    r.add_get(
        '/v1/models/{model_name}/stats', h.model_stats, name='models.stats'
    )
    r.add_get(
        '/v1/models/{model_name}/schema', h.model_detail, name='models.schema'
    )
    r.add_post(
        '/v1/models/{model_name}/predict',
        h.model_predict,
        name='models.predict',
    )
    return api
