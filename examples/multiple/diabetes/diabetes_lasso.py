import pickle
import json

import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV
from mlserve import build_schema


diabetes = datasets.load_diabetes()
X = diabetes.data[:150]
y = diabetes.target[:150]

lasso = Lasso(random_state=0)
alphas = np.logspace(-4, -0.5, 30)

tuned_parameters = [{'alpha': alphas}]
n_folds = 3

clf = GridSearchCV(lasso, tuned_parameters, cv=n_folds, refit=True)
clf.fit(X, y)

scores = clf.cv_results_['mean_test_score']

print(scores)


columns = list(diabetes.feature_names) + ['target']
data = np.c_[diabetes.data, diabetes.target]
df = pd.DataFrame(data=data, columns=columns)


print('Writing model')
with open('diabetes_lasso.pkl', 'wb') as f:
    pickle.dump(clf, f)


print('Writing dataset schema')
schema = build_schema(df)
with open('diabetes_lasso.json', 'w') as f:
    json.dump(schema, f, indent=4, sort_keys=True)
