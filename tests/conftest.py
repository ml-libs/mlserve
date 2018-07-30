import asyncio
import gc

import pytest

from mlserve.main import init


@pytest.fixture(scope='session')
def event_loop():
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    gc.collect()
    loop.close()


@pytest.fixture(scope='session')
def loop(event_loop):
    return event_loop


@pytest.fixture(scope='session')
def model_conf():
    m = {
        "models": [{
        'name': 'boston_gbr_1',
        'model_path': 'tests/data/boston_gbr.pkl',
        'data_schema_path': 'tests/data/boston.json',
        'target': 'target'
    }]}
    return m


@pytest.fixture(scope='session')
def max_workers():
    return 1


@pytest.fixture
def api(loop, aiohttp_client, max_workers, model_conf):
    app = loop.run_until_complete(init(loop, max_workers, model_conf))
    yield loop.run_until_complete(aiohttp_client(app))
    loop.run_until_complete(app.shutdown())


pytest_plugins = []
