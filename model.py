# -*- coding: utf-8 -*-
"""MLModel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KmqitIRAJFDKrQkv-2K6le-eJ8-E4AuR
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

data = pd.read_csv('Crop_recommendation.csv')

data.head()

data.shape

data.isnull().sum()

X = data.iloc[:, :-1]  # Features
y = data.iloc[:, -1]   # Labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train.head()

y_train.head()

model = RandomForestClassifier()

model.fit(X_train, y_train)

predictions = model.predict(X_test)

pickle.dump(model, open("model.pkl", "wb"))

accuracy = model.score(X_test, y_test)

print("Accuracy:", accuracy)

new_features = [[117 ,32,34,26.2724184,52.12739421,6.758792552,127.1752928,]]
predicted_crop = model.predict(new_features)
print("Predicted crop:", predicted_crop)
