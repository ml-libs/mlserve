import pytest
import json
import pandas as pd
import numpy as np
from jsonschema import validate
from mlserve.schema_builder import build_schema


@pytest.fixture(scope='session')
def auto_dataset():
    dataset_path = 'tests/data/Auto.csv'
    df = pd.read_csv(dataset_path)
    return df


@pytest.fixture(scope='session')
def credit_dataset():
    dataset_path = 'tests/data/Credit.csv'
    df = pd.read_csv(dataset_path)

    cat_features = ['Gender', 'Ethnicity', 'Student', 'Married']
    for feature in cat_features:
        df[feature] = df[feature].astype('category')
    return df


def assert_schema(df):
    desc = build_schema(df)
    s = desc['schema']
    ui_schema = desc['ui_schema']
    form_data = desc['example_data']

    for i in range(len(df)):
        row = json.loads(df.iloc[i].to_json())
        validate(row, s)

    assert set(form_data.keys()) == set(df.columns)
    assert ui_schema == {}


def test_basic(auto_dataset, credit_dataset):
    assert_schema(auto_dataset)
    assert_schema(credit_dataset)


def test_none():
    data = {
        'i': [3, 2, 1, np.nan],
        'f': [3.5, 2, 1, np.nan],
        'b': [True, False, True, np.nan],
        's': ['a', 'b', 'c', np.nan],
    }
    df = pd.DataFrame.from_dict(data)
    assert_schema(df)


def test_types():
    data = {
        'i': [3, 2, 1],
        'f': [3.5, 2, 1],
        'b': [True, False, True],
        's': ['a', 'b', 'c'],
    }
    df = pd.DataFrame.from_dict(data)
    assert_schema(df)
