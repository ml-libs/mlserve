import pickle
import json
import numpy as np
import pandas as pd
from sklearn import linear_model, datasets
from sklearn.utils import shuffle
from mlserve import build_schema


iris = datasets.load_iris()

X, y = shuffle(iris.data, iris.target, random_state=13)

offset = int(X.shape[0] * 0.9)
X_train, y_train = X[:offset], y[:offset]
X_test, y_test = X[offset:], y[offset:]

logreg = linear_model.LogisticRegression(C=1e5)
logreg.fit(X, y)

columns = list(iris.feature_names) + ['target']
data = np.c_[iris.data, iris.target]
df = pd.DataFrame(data=data, columns=columns)


print('Writing model')
with open('iris_lr.pkl', 'wb') as f:
    pickle.dump(logreg, f)


print('Writing dataset schema')
schema = build_schema(df)
with open('iris_lr.json', 'w') as f:
    json.dump(schema, f, indent=4, sort_keys=True)
