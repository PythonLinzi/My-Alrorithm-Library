import numpy as np
from numpy import ones, exp, log, dot
from numpy import hstack, round, zeros
import matplotlib.pyplot as plt


class LogitRegression:
    ''' Logistic Regression Algorithm '''
    def __init__(self):
        self.weight = None
        self.features = None
        self.label = None
        return


    def __sigmoid(self, s):
        return 1 / (1 + exp(-s))


    def __log_prob(self, features, target, weights):
        score = dot(features, weights)
        ret = np.sum(target * score - log(1 + exp(score)))
        return ret


    def __show(self):
        w = self.weight
        f = self.features
        label = self.label
        print("Logistic Regression Weights : ", w)
        n, m = self.features.shape
        tmp = hstack((ones((n, 1)), f))
        score = dot(tmp, w)
        preds = round(self.__sigmoid(score))
        cnt = (preds == label).sum().astype(float)
        acc = 100 * cnt / len(preds)
        print('Accuracy : {0}%'.format(acc))
        plt.figure(figsize=(12, 8))
        plt.scatter(f[:, 0], f[:, 1], c=preds == label, alpha=.8, s=50)
        plt.show()
        return


    def train(self, features, label, niter, rate, accept=False):
        '''
        Parameters:
            features: array-like, shape = [n_samples, n_features]
                    Training vector, where n_samples in the number of samples
                    and n_features is the number of features.
            labels: array-like, shape = [n_samples]
                    Target vector for "feature"
            niter: The number of iterations in training (default 100).
            rate: Learning rate.
            accept: Whether add intercept.
        '''
        self.features = features
        self.label = label
        if accept == True:
            tmp = ones((features.shape[0], 1))
            features = hstack((tmp, features))
        weight = zeros(features.shape[1])
        for i in range(niter):
            scores = dot(features, weight)
            preds = self.__sigmoid(scores)
            out_err = label - preds
            grad = dot(features.T, out_err)
            weight += grad * rate
        self.weight = weight
        self.__show()
        return weight # first w[0] is constance


    def predict(self, feature:np.ndarray, label=[]):
        w = self.weight
        f = feature
        n, m = feature.shape
        tmp = hstack((np.ones((n, 1)), f))
        score = dot(tmp, w)
        preds = round(self.__sigmoid(score))
        if len(label):
            cnt = (preds == label).sum().astype(float)
            acc = 100 * cnt / len(preds)
            print('Accuracy : {0}%'.format(acc))
            plt.figure(figsize=(12, 8))
            plt.scatter(f[:, 0], f[:, 1], c=preds == label, alpha=.8, s=50)
            plt.show()
        return preds


# demo1
if __name__ == '__main__':
    def get_demo_data():
        np.random.seed(12)
        num_ = 5000
        x1 = np.random.multivariate_normal([0, 0], [[1, .75], [.75, 1]], num_)
        x2 = np.random.multivariate_normal([1, 4], [[1, .75], [.75, 1]], num_)
        features = np.vstack((x1, x2)).astype(np.float32)
        labels = np.hstack((np.zeros(num_), np.ones(num_)))
        return features, labels


    features, labels = get_demo_data()
    X, y = features[:8000], labels[:8000]
    TestX, Testy = features[8000:], labels[8000:]
    # PLOT RANDOMLY GENERATED DATA
    plt.figure(figsize=(12, 8))
    plt.scatter(features[:, 0], features[:, 1], c=labels, alpha=.4)
    plt.show()

    # WIEGHTS FOR LOGISTIC REGRESSION BUILT FROM SCRATCH
    logit = LogitRegression()
    weights = logit.train(X, y, niter=50000, rate=5e-5, accept=True)
    logit.predict(TestX, Testy)



'''
# demo2
if __name__ == '__main__':
    iris = datasets.load_iris()
    features = iris.data[:, :2]
    labels = (iris.target != 0) * 1
    print(features.shape)

    X, y = features[:100], labels[:100]
    TestX, Testy = features[100:], labels[100:]

    # PLOT RANDOMLY GENERATED DATA
    plt.figure(figsize=(12, 8))
    plt.scatter(features[:, 0], features[:, 1], c=labels, alpha=.4)
    plt.show()

    # WIEGHTS FOR LOGISTIC REGRESSION BUILT FROM SCRATCH
    logit = LogitRegression()
    weights = logit.train(X, y, niter=50000, rate=5e-5, accept=True)
    logit.predict(TestX, Testy)
'''
