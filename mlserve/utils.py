import json
import os

import trafaret as t
import yaml

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, List, Dict


ModelMeta = t.Dict(
    {
        t.Key('name'): t.String,
        t.Key('description'): t.String,
        t.Key('model_path'): t.String,
        t.Key('data_schema_path'): t.String,
        t.Key('target'): t.String,
    }
)


# TODO: rename to something more general
ModelConfig = t.Dict({
    t.Key('host', default='127.0.0.1'): t.String,
    t.Key('port', default=9000): t.Int[0: 65535],
    t.Key('workers', default=2): t.Int[1:127],
    t.Key('models'): t.List(ModelMeta),
})


ServerConfigTrafaret = t.Dict({
    t.Key('host', default='127.0.0.1'): t.String,
    t.Key('port', default=9000): t.Int[0: 65535],
    t.Key('workers', default=2): t.Int[1:127],
}).ignore_extra('*')


@dataclass(frozen=True)
class ServerConfig:
    host: str
    port: int
    workers: int


@dataclass(frozen=True)
class ModelDescriptor:
    name: str
    target: List[str]
    features: List[str]
    schema: Dict[Any, Any]
    model_path: Path
    model_size: int
    data_schema_path: Path
    schema_size: int

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)


def load_model_config(fname: Path) -> Dict[str, Any]:
    with open(fname, 'rt') as f:
        raw_data = yaml.safe_load(f)
    data: Dict[str, Any] = ModelConfig(raw_data)
    return data


def load_models(model_conf: List[Dict[str, str]]) -> List[ModelDescriptor]:
    result: List[ModelDescriptor] = []
    for m in model_conf:
        with open(m['data_schema_path'], 'rb') as f:
            schema = json.load(f)

        target = m['target']
        target: List[str] = target if isinstance(target, list) else [target]
        schema = drop_columns(schema, target)

        schema_size = os.path.getsize(m['data_schema_path'])
        model_size = os.path.getsize(m['model_path'])
        features = list(schema['schema']['properties'].keys())
        model_desc = ModelDescriptor(
            name=m['name'],
            target=target,
            features=features,
            schema=schema,
            model_path=Path(m['model_path']),
            model_size=model_size,
            data_schema_path=Path(m['data_schema_path']),
            schema_size=schema_size,
        )
        result.append(model_desc)
    return result


def drop_columns(schema: Dict[str, Any], columns: List[str]) -> Dict[str, Any]:
    for col in columns:
        schema['schema']['properties'].pop(col, None)
        schema['ui_schema'].pop(col, None)
        schema['example_data'].pop(col, None)

        if col in schema['schema']['required']:
            schema['schema']['required'].remove(col)
    return schema
