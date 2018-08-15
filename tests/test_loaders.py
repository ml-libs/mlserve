from mlserve.loaders import get_loader


def test_pickle_loader():
    model_path = 'tests/data/boston_gbr.pkl'
    loader = get_loader('pickle')
    model = loader(model_path)
    assert hasattr(model, 'predict')


def test_joblib_loader():
    model_path = 'tests/data/boston_gbr.joblib'
    loader = get_loader('joblib')
    model = loader(model_path)
    assert hasattr(model, 'predict')
