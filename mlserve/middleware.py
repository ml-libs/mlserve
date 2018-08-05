import time
from datetime import datetime
from aiohttp.web import middleware
from typing import Awaitable, Callable  # flake8: noqa
from aiohttp.web import HTTPException, Request, Application, Response

from .handlers import APIHandler
from .stats import ModelStats, RequestTiming
from .consts import MODELS_KEY


Handler = Callable[[Request], Awaitable[Response]]


def process_request(
        req: Request, resp: Response, ts: datetime, duration: float
) -> None:
    model_name = req.match_info['model_name']
    if model_name not in req.app[MODELS_KEY]:
        return
    point = RequestTiming(resp.status, ts, duration)
    stats: ModelStats = req.app[MODELS_KEY][model_name]
    stats.log_data_point(point)


@middleware
async def stats_middleware(request: Request, handler: Handler) -> Response:
    if request.match_info.route.name == 'models.predict':
        ts = datetime.now()
        start = time.time()
        try:
            resp = await handler(request)
        except HTTPException as e:
            duration = time.time() - start
            process_request(request, e, ts, duration)
            raise
        else:
            duration = time.time() - start
            process_request(request, resp, ts, duration)

    else:
        resp = await handler(request)
    return resp
