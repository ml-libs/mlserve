import json
import pandas as pd
import numpy as np

import cloudpickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline

from mlserve import build_schema


def read_data(dataset_path):
    class_names = ['toxic', 'severe_toxic', 'obscene',
                   'insult', 'identity_hate']
    train = pd.read_csv(dataset_path).fillna(' ')
    train_text = train[['comment_text']]
    train_targets = train[class_names]
    return train_text, train_targets


class ColumnSelector(BaseEstimator, TransformerMixin):

    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, df):
        return df[self.key]


dataset_path = 'data/train.csv'
train, targets = read_data(dataset_path)
original = pd.concat([train, targets], axis=1)

seed = 1234
word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    stop_words='english',
    ngram_range=(1, 1),
    max_features=10000,
)

logistic = LogisticRegression(C=0.1, solver='sag', random_state=seed)
classifier = MultiOutputClassifier(logistic)

pipeline = Pipeline(steps=[
    ('selector', ColumnSelector(key='comment_text')),
    ('word_tfidf', word_vectorizer),
    ('logistic', classifier)
])


pipeline.fit(train, targets)

scores = cross_val_score(
    pipeline,
    train,
    targets,
    cv=5,
    scoring='roc_auc')

score = np.mean(scores)
print(score)


print('Writing model')
with open('toxic_lr.pkl', 'wb') as f:
    cloudpickle.dump(pipeline, f)


print('Writing dataset schema')
schema = build_schema(original)
with open('toxic_lr.json', 'w') as f:
    json.dump(schema, f, indent=4, sort_keys=True)
