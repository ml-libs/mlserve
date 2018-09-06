import json
import pandas as pd
import cloudpickle
from sklearn.ensemble import RandomForestClassifier
from mlserve import build_schema


columns = [
    'Number.of.posts',
    'Number.of.people.they.follow',
    'Number.of.followers',
    'has_profile_picture',
    'Private.account']
target_name = 'rating'

dtypes = {
    'Number.of.posts': 'uint32',
    'Number.of.people.they.follow': 'uint32',
    'Number.of.followers': 'uint32',
    'has_profile_picture': 'bool',
    'Private.account': 'bool',
}

data = pd.read_csv('labelled_1000_inclprivate.csv', dtype=dtypes)

X_train = data[columns]
y_train = data[target_name]
original = pd.concat([X_train, y_train], axis=1)

rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)
print(rfc.predict_proba(X_train))


print('Writing model')
with open('instgram_rf.pkl', 'wb') as f:
    cloudpickle.dump(rfc, f)


print('Writing dataset schema')
schema = build_schema(original)
with open('instagram.json', 'w') as f:
    json.dump(schema, f, indent=4, sort_keys=True)
