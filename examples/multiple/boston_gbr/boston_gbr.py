import json
import numpy as np
import pandas as pd
import pickle
from sklearn import ensemble
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from mlserve import build_schema

boston = datasets.load_boston()
X, y = shuffle(boston.data, boston.target, random_state=13)
X = X.astype(np.float32)
offset = int(X.shape[0] * 0.9)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

params = {
    'n_estimators': 500,
    'max_depth': 4,
    'min_samples_split': 2,
    'learning_rate': 0.01,
    'loss': 'ls',
}
clf = ensemble.GradientBoostingRegressor(**params)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
mse = mean_squared_error(y_test, clf.predict(X_test))
print('MSE: %.4f' % mse)


columns = list(boston.feature_names) + ['target']
data = np.c_[boston.data, boston.target]
df = pd.DataFrame(data=data, columns=columns)


model_file = 'boston_gbr.pkl'
print('Writing model')
with open(model_file, 'wb') as f:
    pickle.dump(clf, f)


print('Writing dataset schema')
schema = build_schema(df)
with open('boston_schema.json', 'w') as f:
    json.dump(schema, f, indent=4, sort_keys=True)
