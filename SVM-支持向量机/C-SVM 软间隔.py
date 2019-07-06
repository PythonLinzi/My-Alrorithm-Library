''' kernel = ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’ or a callable '''
''' C-Support Vector Machine '''
import numpy as np
from sklearn.svm import SVC


def open_txt(file:str):
    f = open(file=file, mode='r', encoding='UTF-8')
    x, y = [], []
    for line in f:
        tmp = line.split()
        for i, value in enumerate(tmp):
            tmp[i] = float(value)
        x.append(tmp[1:])
        y.append(tmp[0])
    f.close()
    return np.array(x), np.array(y)


X, y = open_txt("fenlei.txt")
X_unknown = X[27:]
X_train, y_train = X[:27], y[:27]

# C [float, optional (default=1.0)]: Penalty parameter C of the error term
clf = SVC(C=1.0, kernel='rbf', gamma='auto', tol=1e-3)
clf.fit(X_train, y_train)
# print(clf.coef_)
print(clf.predict(X_unknown))
