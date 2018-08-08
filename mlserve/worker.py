import pickle  # nosec
import pandas as pd
import json
from typing import Dict, Any, List
from .utils import ModelDescriptor

# TODO: add structural typing with predict method instead
# of Any
_models: Dict[str, Any] = {}


def pickle_loader(model_path: str) -> Any:
    with open(model_path, 'rb') as f:
        pipeline = pickle.load(f)  # nosec
    return pipeline


def warm(models: List[ModelDescriptor]) -> bool:
    global _models
    for model in models:
        if model.name not in _models:
            pipeline = pickle_loader(str(model.model_path))
            _models[model.name] = pipeline
    return True


def predict(model_name: str, raw_data: bytes) -> List[float]:
    # TODO: wrap this call into try except
    df = pd.DataFrame(json.loads(raw_data))
    results: List[float] = _models[model_name].predict(df).tolist()
    return results
