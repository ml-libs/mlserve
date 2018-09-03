import json
from typing import Dict, Any, List, Optional

import numpy as np
import pandas as pd

from .loaders import get_loader
from .utils import ModelDescriptor


# TODO: add structural typing with predict method instead
# of Any
Cache = Dict[str, Any]
_models: Cache = {}


def warm(models: List[ModelDescriptor], cache: Optional[Cache]=None) -> bool:
    global _models
    cache = cache if cache is not None else _models

    for model in models:
        loader = get_loader(model.loader)
        if model.name not in cache:
            pipeline = loader(str(model.model_path))
            cache[model.name] = pipeline
    return True


def format_result(
        pred: np.ndarray, target: List[str]) -> List[Dict[str, float]]:
    if len(target) == 1:
        results_list = [pred]
    else:
        results_list = pred

    formated = []
    for r in results_list:
        paris = [(t, r) for t, r in zip(target, r)]
        formated.append(dict(paris))
    return formated


def predict(
        model_name: str, target: List[str], raw_data: bytes,
        cache: Optional[Cache]=None
) -> List[Dict[str, float]]:
    cache = cache if cache is not None else _models
    # TODO: wrap this call into try except
    df = pd.DataFrame(json.loads(raw_data))
    model = cache[model_name]
    results: List[float]
    if hasattr(model, 'predict_proba'):
        results = model.predict_proba(df)
        results = np.array(results).T[1].tolist()
    else:
        results = model.predict(df)

    return format_result(results, target)
