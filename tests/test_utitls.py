from unittest import mock
from pathlib import Path

from mlserve.utils import load_models, ModelDescriptor

schema = {
    'properties': {
        'AGE': {'type': ['number']},
        'B': {'type': ['number']},
        'CHAS': {'type': ['number']},
        'CRIM': {'type': ['number']},
        'DIS': {'type': ['number']},
        'INDUS': {'type': ['number']},
        'LSTAT': {'type': ['number']},
        'NOX': {'type': ['number']},
        'PTRATIO': {'type': ['number']},
        'RAD': {'type': ['number']},
        'RM': {'type': ['number']},
        'TAX': {'type': ['number']},
        'ZN': {'type': ['number']},
        'target': {'type': ['number']},
    },
    'required': [
        'CRIM',
        'ZN',
        'INDUS',
        'CHAS',
        'NOX',
        'RM',
        'AGE',
        'DIS',
        'RAD',
        'TAX',
        'PTRATIO',
        'B',
        'LSTAT',
        'target',
    ],
    'type': 'object',
}


def test_load_models():
    m = [
        {
            'name': 'boston_gbr_1',
            'model_path': 'tests/data/boston_gbr.pkl',
            'data_schema_path': 'tests/data/boston.json',
            'target': 'target',
        }
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
        'target',
    ]
    m = ModelDescriptor(
        name='boston_gbr_1',
        features=f,
        schema=schema,
        target='target',
        model_path=Path('tests/data/boston_gbr.pkl'),
        model_size=mock.ANY,
        data_schema_path=Path('tests/data/boston.json'),
        schema_size=mock.ANY,
    )
    assert [m] == r
