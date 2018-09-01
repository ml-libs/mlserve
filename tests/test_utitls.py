import json
from pathlib import Path

import pytest
from mlserve.utils import load_models, ModelMeta
from mlserve.worker import warm, predict


def test_load_models():
    m = [
        ModelMeta({
            'name': 'boston_gbr_1',
            'description': 'model predicts',
            'model_path': 'tests/data/boston_gbr.pkl',
            'data_schema_path': 'tests/data/boston.json',
            'target': 'target',
        })
    ]
    r = load_models(m)
    f = [
        'AGE',
        'B',
        'CHAS',
        'CRIM',
        'DIS',
        'INDUS',
        'LSTAT',
        'NOX',
        'PTRATIO',
        'RAD',
        'RM',
        'TAX',
        'ZN',
    ]
    assert len(r) == 1
    model_desc = r[0]
    assert model_desc.loader == 'pickle'
    assert model_desc.target == ['target']
    assert model_desc.name == 'boston_gbr_1'
    assert model_desc.features == f
    assert model_desc.model_path == Path('tests/data/boston_gbr.pkl')
    assert model_desc.data_schema_path == Path('tests/data/boston.json')


@pytest.fixture
def model_desc():
    m = [
        ModelMeta({
            'name': 'boston_gbr_1',
            'description': 'model predicts',
            'model_path': 'tests/data/boston_gbr.pkl',
            'data_schema_path': 'tests/data/boston.json',
            'target': 'target',
        })
    ]
    r = load_models(m)
    assert len(r) == 1
    return r[0]


def test_warm_predict(model_desc):
    cache = {}
    warm([model_desc], cache)
    assert len(cache) == 1
    raw = json.dumps([model_desc.schema['example_data']])
    target = ['target']

    result = predict(model_desc.name, target, raw, cache)
    assert result
