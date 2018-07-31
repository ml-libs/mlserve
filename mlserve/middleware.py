from aiohttp.web import middleware


@middleware
async def stats_middleware(request, handler):
    resp = await handler(request)
    return resp
