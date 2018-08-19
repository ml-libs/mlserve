import pickle  # nosec
from typing import Any, Callable


def pickle_loader(model_path: str) -> Any:
    with open(model_path, 'rb') as f:
        pipeline = pickle.load(f)  # nosec
    return pipeline


def joblib_loader(model_path: str) -> Any:
    from sklearn.externals import joblib
    with open(model_path, 'rb') as f:
        pipeline = joblib.load(f)  # nosec
    return pipeline


def get_loader(loader_name: str) -> Callable[[str], Any]:
    if loader_name == 'joblib':
        return joblib_loader
    return pickle_loader
