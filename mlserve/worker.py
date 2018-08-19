import numpy as np
import pandas as pd
import json
from typing import Dict, Any, List
from .utils import ModelDescriptor
from .loaders import get_loader


# TODO: add structural typing with predict method instead
# of Any
_models: Dict[str, Any] = {}


def warm(models: List[ModelDescriptor]) -> bool:
    global _models
    for model in models:
        loader = get_loader(model.loader)
        if model.name not in _models:
            pipeline = loader(str(model.model_path))
            _models[model.name] = pipeline
    return True


def predict(model_name: str, raw_data: bytes) -> List[float]:
    # TODO: wrap this call into try except
    df = pd.DataFrame(json.loads(raw_data))
    model = _models[model_name]
    results: List[float]
    if hasattr(model, 'predict_proba'):
        results = model.predict_proba(df)
        results = np.array(results).T[1].tolist()
    else:
        results = model.predict(df).tolist()
    return results
