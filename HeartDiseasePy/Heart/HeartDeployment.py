import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from matplotlib import pyplot as plt
import os
import pickle
from sklearn.model_selection import train_test_split

df = pd.read_csv("heart.csv")

print(df.head())

print(df.info())


df.isnull().values.any()
df["target"].value_counts().plot(kind='bar', color=["salmon","lightblue"])
plt.show()

X = df[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs','restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]

y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

# Train the model
classifier = MLPClassifier()
#classifier = MLPClassifier(max_iter=500)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))

clreport = classification_report(y_test, y_pred)

print("Accuracy on training set: {:.2f}".format(classifier.score(X_train, y_train)))
print("Accuracy on test set: {:.2f}".format(classifier.score(X_test, y_test)))


# Creating a pickle file for the classifier
filename = 'heart-model.pkl'
pickle.dump(classifier, open(filename, 'wb'))
