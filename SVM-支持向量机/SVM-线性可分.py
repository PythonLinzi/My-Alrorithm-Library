from sklearn.svm import LinearSVC
from sklearn.datasets import make_classification as mc

'''
若抛出以下 Warning 很可能代表线性不可分, 需要考虑线性近似或非线性的可分
ConvergenceWarning: Liblinear failed to converge, increase the number of iterations.
"the number of iterations.", ConvergenceWarning)
'''

x, y = mc(n_samples=100, n_features=4, random_state=0)
clf = LinearSVC(random_state=0, max_iter=1000, tol=1e-5)
clf.fit(x, y)
coef = clf.coef_ # 获取分类函数系数 Matrix
print(coef)
print("分类函数为 C(X) = %fx1 + %fx2 + %fx3 + %fx4" % (coef[0][0], coef[0][1], coef[0][2], coef[0][3]))
x_unknown = [[0, 0.498481, -0.394148, 0]] # 待分类测试数据
y_predict = clf.predict(x_unknown) # 分类结果
print(y_predict) # C(X)>=0即为第一类0, C(X)<0则为第二类1
