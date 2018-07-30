async def test_index_page(api):
    resp = await api.get('/')
    assert resp.status == 200
    body = await resp.text()
    assert body


async def test_models_list(api):
    resp = await api.get('/api/v1/models')
    assert resp.status == 200
    body = await resp.json()
    assert isinstance(body, list)
    assert len(body) == 1


async def test_get_one_model(api):
    resp = await api.get('/api/v1/models/boston_gbr_1')
    assert resp.status == 200
    body = await resp.json()
    assert isinstance(body, dict)

    resp = await api.get('/api/v1/models/no_such_model')
    assert resp.status == 404
    body = await resp.json()
    assert isinstance(body, dict)


preds = {
    'CRIM': {'0': 0.00632},
    'ZN': {'0': 18.0},
    'INDUS': {'0': 2.31},
    'CHAS': {'0': 0.0},
    'NOX': {'0': 0.538},
    'RM': {'0': 6.575},
    'AGE': {'0': 65.2},
    'DIS': {'0': 4.09},
    'RAD': {'0': 1.0},
    'TAX': {'0': 296.0},
    'PTRATIO': {'0': 15.3},
    'B': {'0': 396.9},
    'LSTAT': {'0': 4.98},
}


async def test_baic_predict(api):
    resp = await api.post('/api/v1/models/no_such_model/predict', json=preds)
    assert resp.status == 404
    body = await resp.json()
    assert isinstance(body, dict)

    resp = await api.post('/api/v1/models/boston_gbr_1/predict', json=preds)
    assert resp.status == 200
    body = await resp.json()
    assert isinstance(body, list)
