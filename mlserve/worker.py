import pickle  # nosec
import pandas as pd
from typing import Dict, Any, List


_models: Dict[str, Any] = {}


def warm(models) -> bool:
    global _models
    for model in models:
        if model.name not in _models:
            with open(model.model_path, 'rb') as f:
                pipeline = pickle.load(f)  # nosec
            _models[model.name] = pipeline
    return True


def predict(model_name: str, raw_data) -> List[float]:
    df = pd.read_json(raw_data)
    results = _models[model_name].predict(df)
    return results.tolist()
