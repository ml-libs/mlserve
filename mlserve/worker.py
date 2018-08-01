import pickle  # nosec
import pandas as pd
from typing import Dict, Any, List


_models: Dict[str, Any] = {}


def pickle_loader(model_path: str) -> Any:
    with open(model_path, 'rb') as f:
        pipeline = pickle.load(f)  # nosec
    return pipeline


def warm(models) -> bool:
    global _models
    for model in models:
        if model.name not in _models:
            pipeline = pickle_loader(model.model_path)
            _models[model.name] = pipeline
    return True


def predict(model_name: str, raw_data) -> List[float]:
    df = pd.read_json(raw_data)
    results = _models[model_name].predict(df)
    return results.tolist()
