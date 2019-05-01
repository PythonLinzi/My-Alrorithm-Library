import numpy as np
from random import randrange
from sklearn.cluster import KMeans

X = np.array([[1, 1, 1, 1, 1, 1, 1],
              [2, 3, 2, 2, 2, 2, 2],
              [3, 2, 3, 3, 3, 3, 3],
              [1, 2, 1, 2, 2, 1, 2],
              [2, 1, 3, 3, 3, 2, 1],
              [6, 2, 30, 3, 33, 2, 71]])
#  train
kmeans_predicter = KMeans(n_clusters=3).fit(X)
#  raw data classification
category = kmeans_predicter.predict(X)
print('分类情况:',category)
print('='*30)

def predict(element):
    result = kmeans_predicter.predict(element)
    print('预测结果:',result)
    print('相似元素:\n',X[category == result])

#  test
predict([[1, 2, 3, 3, 1, 3, 1]])
print('='*30)
predict([[5, 2, 23, 2, 21, 5, 51]])
