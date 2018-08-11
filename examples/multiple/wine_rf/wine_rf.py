import pandas as pd

import mlserve
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score


dataset_url = (
    'http://mlr.cs.umass.edu/'
    'ml/machine-learning-databases/'
    'wine-quality/winequality-red.csv'
)
data = pd.read_csv(dataset_url, sep=';')


y = data.quality
X = data.drop('quality', axis=1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123, stratify=y
)

pipeline = make_pipeline(
    StandardScaler(), RandomForestRegressor(n_estimators=100)
)

hyperparameters = {
    'randomforestregressor__max_features': ['auto', 'sqrt', 'log2'],
    'randomforestregressor__max_depth': [None, 5],
}

clf = GridSearchCV(pipeline, hyperparameters, cv=5)
clf.fit(X_train, y_train)

pred = clf.predict(X_test)
print(r2_score(y_test, pred))
print(mean_squared_error(y_test, pred))

model_file = 'wine_quality_rf.pkl'
print('Writing model')
with open(model_file, 'wb') as f:
    pickle.dump(clf, f)


print('Writing dataset schema')
schema = mlserve.build_schema(data)
with open('wine_quality_schema.json', 'w') as f:
    json.dump(schema, f, indent=4, sort_keys=True)
