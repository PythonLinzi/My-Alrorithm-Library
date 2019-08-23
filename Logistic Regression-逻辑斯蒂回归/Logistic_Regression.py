import numpy as np
from numpy import ones, exp, log, dot
from numpy import hstack, round, zeros
from numpy import meshgrid, linspace, vstack
from numpy.random import rand
import matplotlib.pyplot as plt
from scipy.optimize import dual_annealing as DA
from scipy.optimize import differential_evolution as DE


class LogitRegression:
    ''' Logistic Regression '''
    def __init__(self, features, label):
        '''
        :param features: array-like, shape = [n_samples, n_features]
                    Training vector, where n_samples in the number of samples
                    and n_features is the number of features.
        :param label: array-like, shape = [n_samples]
                    Target vector for "feature"
        '''
        self.weight = None
        self.features = features
        self.label = label
        self.n, self.m = features.shape
        self.bnd = (-100, 100)
        return


    def __sigmoid(self, s):
        return 1 / (1 + exp(-s))


    def __log_likehood(self, X, y, w):
        '''
        :param X: array-like, shape = [n_samples, n_features]
        :param y: array-like, shape = [n_samples], denotes label/category
        :param w: array-like, shape = [n_features + 1]
        :return ret: float, log-likehood, target which need be minimized
        '''
        score = dot(X, w)
        ret = np.sum(-y * score + log(1 + exp(score)))
        return ret


    def __grad(self, niter=5e4, rate=5e-5, accept=True):
        '''
        Gradient Descent Method
        :param niter: int, The number of iterations in training(default 5w)
        :param rate: float, Learning rate
        :param accept: bool, Whether add intercept b (wx+b)
        :return w: array-like, shape = [n_features + 1], weights
        '''
        niter = int(niter)
        features = self.features
        label = self.label
        self.n, self.m = features.shape
        if accept == True:
            tmp = ones((self.n, 1))
            features = hstack((tmp, features))
        w = zeros(features.shape[1])
        for i in range(niter):
            scores = dot(features, w)
            preds = self.__sigmoid(scores)
            out_err = label - preds
            grad = dot(features.T, out_err)
            w += grad * rate
        print("Global Best Wights =", w)
        return w


    def __DA(self, func, niter=1000):
        '''
        Dual_Annealing Algorithm
        :param func: Target function (Min)
        :param niter: int, the number of iterations in training(default 1k)
        :return w: array-like, shape = [n_features + 1], weights
        '''
        m = self.m + 1
        bnd = self.bnd
        bnds = [bnd] * m
        res = DA(func=func, bounds=bnds, maxiter=niter, seed=623)
        s1 = "Global Best Wights = {0}\n"
        s2 = "Log-likehood(weight) = {1:.6f}"
        show = s1 + s2
        print(show.format(res.x, res.fun))
        w = res.x
        return w


    def __DE(self, func, niter=1000):
        '''
        Differential Evolution Algorithm
        :param func: Target function (Min)
        :param niter: int, the number of iterations in training(default 1k)
        :return w: array-like, shape = [n_features + 1], weights
        '''
        bnd = self.bnd
        m = self.m + 1
        bnds = [bnd] * m
        res = DE(func=func, bounds=bnds, maxiter=niter, popsize=25,
                 tol=0.01, mutation=(0.5, 1), recombination=0.7)
        s1 = "Global Best Wights = {0}\n"
        s2 = "Log-likehood(weight) = {1:.6f}"
        show = s1 + s2
        print(show.format(res.x, res.fun))
        w = res.x
        return w


    def __PSO(self, func, niter=1000):
        '''
        Particle Swarm Optimization Algorithm
        :param func: Target function (Min)
        :param niter: int, the number of iterations in training(default 1k)
        :return w: array-like, shape = [n_features + 1], weights
        '''
        n = self.m + 1  # demensions 维数
        N = 50
        vmin, vmax = -1, 1
        w, c1, c2 = 1, 2, 2.1
        c = c1 + c2
        K = 2 / (np.abs(2 - c - np.sqrt(c * c - 4 * c)))
        x, v = rand(N, n), rand(N, n)  # 注意初始值X要在取值范围内随机投点
        y = np.array([func(v) for v in x])
        pbest_x, pbest_y = x.copy(), y.copy()
        gbest_x, gbest_y = x[y.argmin()], y.min()
        for _ in range(niter):
            for i in range(N):
                for j in range(n):
                    pb = c1 * rand(1) * (pbest_x[i][j] - x[i][j])
                    gb = c2 * rand(1) * (gbest_x[j] - x[i][j])
                    v[i][j] = K * (v[i][j] + pb + gb)
                    v[i][j] = min(v[i][j], vmax)
                    v[i][j] = max(v[i][j], vmin)
                x[i] += v[i]
                y[i] = func(x[i])
                if y[i] < pbest_y[i]:
                    pbest_x[i], pbest_y[i] = x[i], y[i]
                if y[i] < gbest_y:
                    gbest_x, gbest_y = x[i], y[i]
        s1 = "Global Best Wights = {0}\n"
        s2 = "Log-likehood(weight) = {1:.6f}"
        show = s1 + s2
        print(show.format(gbest_x, gbest_y))
        w = gbest_x
        return w


    def __optimize(self, method='DA', niter=1000):
        '''
        Optimition method instead of Gradient Descent method
        :param method: str, optimization method, "DA","DA","PSO"
        :param niter: int, the number of iterations in training(default 1k)
        :return w: array-like, shape = [n_features + 1], weights
        '''
        np.seterr(over='ignore')
        one = ones((self.n, 1))
        X = hstack((one, self.features))
        y = self.label
        def f(w):
            ret = self.__log_likehood(X, y, w)
            return ret
        if method == 'DA':
            w = self.__DA(func=f, niter=niter)
        elif method == 'DE':
            w = self.__DE(func=f, niter=niter)
        elif method == 'PSO':
            w = self.__PSO(func=f, niter=niter)
        return w


    def train(self, method='grad', niter=1000):
        '''
        Train
        :param method: str, training method, "DA","DA","PSO"
        :param niter: int, the number of iterations in training(default 1k)
        :return w: array-like, shape = [n_features + 1], weights
        '''
        print('------------- Training -------------')
        if method == 'grad':
            w = self.__grad(niter=niter, accept=True)
        else:
            w = self.__optimize(method, niter)
        self.weight = w
        self.__print_func(w)
        self.__show(self.features, self.label)
        return w # first w[0] is constance


    def predict(self, feature:np.ndarray, label=[]):
        '''
        prediction
        :param feature: array-like, shape = [n_samples, n_features]
        :param label: array-like, shape = [n_samples]
        :return preds: array-like, shape = [n_samples], label predicted
        '''
        w = self.weight
        f = feature
        n, m = feature.shape
        tmp = hstack((np.ones((n, 1)), f))
        score = dot(tmp, w)
        preds = round(self.__sigmoid(score))
        print()
        print('------------- Prediction -------------')
        print('Labels:', end=' ')
        print(preds)
        if len(label):
            self.__show(f, label, False)
        return preds # label predicted


    def __print_func(self, w):
        '''
        :param w: weights
        :return:
        '''
        print()
        print('------------- Classfication Function -------------')
        WX = str(w[0])
        for i in range(1, self.m + 1):
            if w[i] > 0:
                WX += (' + ' + str(w[i]) + 'x' + str(i))
            elif w[i] < 0:
                WX += (' - ' + str(-w[i]) + 'x' + str(i))
            else:
                continue
        print("y = 1 / (1 + exp(-(" + WX + ")))")
        print()
        return


    def __show(self, features:np.ndarray, label:np.ndarray, reg=True):
        '''
        :param features: array-like, shape = [n_samples, n_features]
        :param label: array-like, shape = [n_samples]
        :param reg: bool, judging for reg or pred
        :return:
        '''
        w = self.weight
        f = features
        label = label
        n = features.shape[0]
        one = ones((n, 1))
        tmp = hstack((one, f))
        score = dot(tmp, w)
        probs = self.__sigmoid(score) # probability
        preds = round(probs) # label predicted
        cnt = (preds == label).sum().astype(float)
        acc = 100 * cnt / len(preds)
        if reg:
            print('Regression Accuracy : {0}%'.format(acc))
        else:
            print('Prediction Accuracy : {0}%'.format(acc))
        # 二维图像可能无法展示分割
        if len(w) == 3:
            c1x, c1y = [], []
            c2x, c2y = [], []
            for i, ca in enumerate(preds):
                if ca == 0:
                    c1x.append(f[i][0])
                    c1y.append(f[i][1])
                else:
                    c2x.append(f[i][0])
                    c2y.append(f[i][1])
            plt.scatter(c1x, c1y, c='r', alpha=0.7, s=15, label='Type_1')
            plt.scatter(c2x, c2y, c='b', alpha=0.7, s=15, label='Type_2')
            x1min = np.min(features, axis=0)[0]
            x1max = np.max(features, axis=0)[0]
            x2min = np.min(features, axis=0)[1]
            x2max = np.max(features, axis=0)[1]
            (xx1, xx2) = meshgrid(linspace(x1min, x1max), linspace(x2min, x2max))
            grid_ = np.c_[xx1.ravel(), xx2.ravel()]
            one_ = ones((grid_.shape[0], 1))
            grid_ = hstack((one_, grid_))
            prob_ = dot(grid_, w)
            prob_ = prob_.reshape(xx1.shape)
            plt.contour(xx1, xx2, prob_, [0.5], linewidths=5, colors='black')
            plt.xlabel('X1')
            plt.ylabel('X2')
            plt.legend()
            plt.grid()
            plt.show()
        return




if __name__ == '__main__':
    def demo1_data():
        np.random.seed(12)
        num_ = 5000
        x1 = np.random.multivariate_normal([0, 0], [[1, .75], [.75, 1]], num_)
        x2 = np.random.multivariate_normal([1, 4], [[1, .75], [.75, 1]], num_)
        features = np.vstack((x1, x2)).astype(np.float32)
        labels = np.hstack((np.zeros(num_), np.ones(num_)))
        X, y = features[:8000], labels[:8000]
        TestX, Testy = features[8000:], labels[8000:]
        return X, y, TestX, Testy

    def demo2_data():
        from sklearn import datasets
        iris = datasets.load_iris()
        features = iris.data[:, :2]
        labels = (iris.target != 0) * 1
        X, y = features[:100], labels[:100]
        TestX, Testy = features[100:], labels[100:]
        return X, y, TestX, Testy

    def demo3_data():
        # Num of samples
        N = 100
        # Label vector
        label4training = vstack((zeros((N, 1)), ones((N, 1))))
        label4test = vstack((zeros((N, 1)), ones((N, 1))))
        # Features
        feature4class1 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        feature4class2 = np.array([-1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        feature4training = vstack(((
            dot(ones((N, 1)), [feature4class1]),
            dot(ones((N, 1)), [feature4class2]))))
        feature4test = vstack(((
            dot(ones((N, 1)), [feature4class1]),
            dot(ones((N, 1)), [feature4class2]))))
        np.random.seed(seed=1)
        feature4training += 0.5 * np.random.randn(*feature4training.shape)
        feature4test += 0.5 * np.random.randn(*feature4test.shape)
        X, y = feature4training, label4training.flatten()
        TestX, Testy = feature4test, label4test.flatten()
        return X, y, TestX, Testy

    #X, y, TestX, Testy = demo1_data()
    #X, y, TestX, Testy = demo2_data()
    X, y, TestX, Testy = demo3_data()
    demo3_data()
    logit = LogitRegression(X, y)
    weights = logit.train(method='PSO', niter=200)
    logit.predict(TestX, Testy)

