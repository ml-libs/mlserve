from pathlib import Path

from mlserve.utils import load_models, ModelMeta
from mlserve.worker import warm


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


def test_warm():
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
    cache = {}
    warm(r, cache)
    assert len(cache) == 1
