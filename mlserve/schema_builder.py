import json
import pandas as pd

from pandas.core.dtypes.common import (
    is_bool_dtype,
    is_categorical_dtype,
    is_datetime64_dtype,
    is_datetime64tz_dtype,
    is_integer_dtype,
    is_numeric_dtype,
    is_period_dtype,
    is_string_dtype,
    is_timedelta64_dtype,
)
from typing import Dict, Any, List, Optional


def as_json_table_type(x) -> str:
    if is_integer_dtype(x):
        return 'integer'
    elif is_bool_dtype(x):
        return 'boolean'
    elif is_numeric_dtype(x):
        return 'number'
    elif (
        is_datetime64_dtype(x)
        or is_datetime64tz_dtype(x)
        or is_period_dtype(x)
    ):
        # TODO: fix this
        # return 'datetime'
        return 'string'
    elif is_timedelta64_dtype(x):
        # TODO: fix this
        # return 'duration'
        return 'string'
    elif is_categorical_dtype(x):
        # TODO: fix this
        # return 'any'
        return 'string'
    elif is_string_dtype(x):
        return 'string'
    else:
        return 'any'


text_area = {
    'ui:widget': 'textarea',
    'ui:options': {
        'rows': 10
    }
}


radio_button = {'ui:widget': 'radio'}


def make_field(arr: pd.Series):
    ui_schema: Optional[Dict[str, Any]] = None
    add_types = []
    if arr.isnull().sum() > 0:
        arr_no_na = arr.dropna()
        dtype = arr_no_na.infer_objects().dtypes
        add_types.append('null')
    else:
        dtype = arr.dtype

    if arr.name is None:
        name = 'values'
    else:
        name = arr.name
    json_type = as_json_table_type(dtype)
    field = {'type': [as_json_table_type(dtype)] + add_types}

    if json_type == 'string' and arr.str.len().mean() > 50:
        ui_schema = text_area

    if is_categorical_dtype(arr):
        if hasattr(arr, 'categories'):
            cats = arr.categories
            # ordered = arr.ordered
        else:
            cats = arr.cat.categories
            # ordered = arr.cat.ordered
        field['enum'] = list(cats)

    # TODO: handle datetime properly
    # elif is_period_dtype(arr):
    #     field['freq'] = arr.freqstr

    # elif is_datetime64tz_dtype(arr):
    #     if hasattr(arr, 'dt'):
    #         field['tz'] = arr.dt.tz.zone
    #     else:
    #         field['tz'] = arr.tz.zone
    return name, field, dtype, ui_schema


def build_schema(
        data: pd.DataFrame, include_example: bool=True
) -> Dict[str, Any]:
    form_data = json.loads(data.iloc[[0]].to_json(orient='records'))[0]
    fields = []
    for _, s in data.items():
        fields.append(make_field(s))

    names: List[str] = []
    items = {}
    ui_schema: Dict[str, Any] = {}
    for k, v, _, ui in fields:
        items[k] = v
        # if 'null' not in v['type']:
        names.append(k)
        if ui is not None:
            ui_schema[k] = ui

    schema = {'type': 'object', 'properties': items, 'required': names}
    result = {
        'schema': schema,
        'ui_schema': ui_schema,
        'example_data': form_data if include_example else {},
    }
    return result
