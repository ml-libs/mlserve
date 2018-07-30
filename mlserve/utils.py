import asyncio
import signal
import json
import os

import trafaret as t
import yaml

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, List, Dict
from .worker import warm


ModelMeta = t.Dict({
    t.Key('name'): t.String,
    t.Key('description'): t.String,
    t.Key('model_path'): t.String,
    t.Key('data_schema_path'): t.String,
    t.Key('target'): t.String,
})

ModelConfig = t.Dict({t.Key('models'): t.List(ModelMeta)})


def load_model_config(fname):
    with open(fname, 'rt') as f:
        raw_data = yaml.safe_load(f)
    data = ModelConfig(raw_data)
    return data


async def setup_executor(app, max_workers, models):
    n = max_workers
    executor = ProcessPoolExecutor(max_workers=n)
    loop = asyncio.get_event_loop()
    run = loop.run_in_executor
    fs = [run(executor, warm, models) for i in range(0, n)]
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
