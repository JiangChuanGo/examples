import numpy as np
import pandas as pd
import mglearn

from sklearn.neighbors import KNeighborsClassifier 
from sklearn.model_selection import train_test_split 

from sklearn.datasets import load_iris 


iris_dataset = load_iris()

print("Keys of iris_dataset: \n{}".format(iris_dataset.keys()))

print("Feature names: \n{}".format(iris_dataset['feature_names']))

X_train, X_test, y_train, y_test = train_test_split(
iris_dataset['data'], iris_dataset['target'], random_state=0)

print("X_train shape: {}".format(X_train.shape))
print("y_train shape: {}".format(y_train.shape))

iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
# 按y_train着色
grr = pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker='o',
hist_kwds={'bins': 20}, s=60, alpha=.8, cmap=mglearn.cm3)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
print("Test set predictions:\n {}".format(y_pred))
print("Test set score: {:.2f}".format(np.mean(y_pred == y_test)))
