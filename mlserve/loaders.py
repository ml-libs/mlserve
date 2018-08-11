import pickle  # nosec
from typing import Any


def pickle_loader(model_path: str) -> Any:
    with open(model_path, 'rb') as f:
        pipeline = pickle.load(f)  # nosec
    return pipeline


def joblib_loader(model_path: str) -> Any:
    from sklearn.externals import joblib
    with open(model_path, 'rb') as f:
        pipeline = joblib.load(f)  # nosec
    return pipeline


def dill_loader(model_path: str) -> Any:
    import dill
    with open(model_path, 'rb') as f:
        pipeline = dill.load(f)  # nosec
    return pipeline


def get_loader(loader_name):
    if loader_name == 'joblib':
        return joblib_loader
    if loader_name == 'dill':
        return dill_loader
    else:
        return pickle_loader
