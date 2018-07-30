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


def as_json_table_type(x):
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


def make_field(arr):
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

    field = {'type': [as_json_table_type(dtype)] + add_types}

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
    return name, field


def build_schema(data):
    fields = []
    for _, s in data.items():
        fields.append(make_field(s))

    names = []
    items = {}
    for k, v in fields:
        items[k] = v
        # if 'null' not in v['type']:
        names.append(k)

    schema = {'type': 'object', 'properties': items, 'required': names}
    return schema
