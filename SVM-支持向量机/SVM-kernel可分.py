''' kernel = ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable '''
''' gamma = 'auto' or 'scale' '''

import numpy as np
X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
y = np.array([1, 1, 2, 2])

from sklearn.svm import NuSVC

# poly 多项式核函数
# degree [int, optional (default=3)]: Degree of the polynomial kernel function (‘poly’).
# Ignored by all other kernels.
clf = NuSVC(kernel='poly', degree=3, gamma='auto', nu=0.5, tol=0.001)
clf.fit(X, y)
print(clf.predict([[-0.8, -1]]))
print(clf.get_params())


# rbf 径向基核函数
clf = NuSVC(kernel='rbf', gamma='scale', nu=0.5, tol=1e-3)
clf.fit(X, y)
print(clf.predict([[-0.8, -1]]))


# sigmoid S型内核函数
clf = NuSVC(kernel='sigmoid', gamma='scale', tol=0.001)
clf.fit(X, y)
print(clf.predict([[-0.8, -1]]))
