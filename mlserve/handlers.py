import asyncio
import json
from aiohttp import web
from pathlib import Path
from functools import partial

from .exceptions import ObjectNotFound
from .worker import predict


jsonify = partial(json.dumps, indent=4, sort_keys=True)
json_response = partial(web.json_response, dumps=jsonify)


class Handler:
    def __init__(self, executor, project_root, model_desc):
        self._executor = executor
        self._root = project_root
        self._loop = asyncio.get_event_loop()
        self._models = {m.name: m for m in model_desc}

    def validate_model_name(self, model_name: str) -> str:
        if model_name not in self._models:
            msg = f'Model with name {model_name} not found.'
            raise ObjectNotFound(msg)
        return model_name

    async def index(self, request):
        path = str(self._root / 'static' / 'index.html')
        return web.FileResponse(path)

    # API
    async def model_list(self, request):
        result = sorted(self._models.values(), key=lambda v: v.name)
        r = [{'name': m.name, 'target': m.target} for m in result]
        return json_response(r)

    async def model_detail(self, request):
        model_name = request.match_info['model_name']
        self.validate_model_name(model_name)

        r = self._models[model_name].asdict()
        return json_response(r)

    async def model_predict(self, request):
        model_name = request.match_info['model_name']
        self.validate_model_name(model_name)

        raw_data = await request.read()
        run = self._loop.run_in_executor
        r = await run(self._executor, predict, model_name, raw_data)
        return json_response(r)


def setup_routes(
    app: web.Application, handler: Handler, project_root: Path
) -> web.Application:
    r = app.router
    h = handler
    path = str(project_root / 'static')
    r.add_get('/', h.index, name='index')
    r.add_static('/static/', path=path, name='static')
    # api
    r.add_get('/api/v1/models', h.model_list, name='model.list')
    r.add_get(
        '/api/v1/models/{model_name}', h.model_detail, name='model.detail'
    )
    r.add_post(
        '/api/v1/models/{model_name}/predict',
        h.model_predict,
        name='model.predict',
    )
    return app
