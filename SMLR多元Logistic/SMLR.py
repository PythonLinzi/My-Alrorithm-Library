import numpy as np
from numpy import vstack, ones, zeros, delete
from numpy import unique, hstack, where
from numpy import transpose, exp, dot
from numpy import newaxis, argmax, linalg
from numpy import array, log, nonzero
from numpy import squeeze, diag, kron, sum, all
from sklearn.base import ClassifierMixin
from sklearn.base import BaseEstimator
import matplotlib.pyplot as plt
from scipy.optimize import minimize


class SMLR(BaseEstimator, ClassifierMixin):
    """Sparce Multinomial Logistic Regression (SMLR) classifier.

    The API of this function is compatible with the logistic regression in
    scikit-learn.

    Parameters:
        max_iter: The maximum number of iterations in training
            (default 1000; int).
        n_iter: The number of iterations in training (default 100).
        verbose: If 1, print verbose information (default).

    Attributes:
        `coef_`: array, shape = [n_classes, n_features]
            Coefficient of the features in the decision function.
        `intercept_`: array, shape = [n_classes]
            Intercept (a.k.a. bias) added to the decision function.
    """

    def __init__(self, max_iter=1000, tol=1e-5, verbose=1):
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        # self.densify

        print("SMLR (sparse multinomial logistic regression)")

    def fit(self, feature, label):
        """fit(self, feature, label) method of SMLR instance

        Fit the model according to the given training data (in the same way as
        logistic.py in sklearn).

        Parameters:
            feature: array-like, shape = [n_samples, n_features]
                    Training vector, where n_samples in the number of samples
                    and n_features is the number of features.
            label: array-like, shape = [n_samples]
                    Target vector for "feature"

        Returns:
            self: object
            Returns self.
        """

        # feature: matrix, whose size is # of samples by # of dimensions.
        # label: label vector, whose size is # of samples.
        # If you treat a classification problem with C classes, please
        # use 0,1,2,...,(C-1) to indicate classes

        # Check # of features, # of dimensions, and # of classes
        self.classes_, indices = unique(label, return_inverse=True)
        N = feature.shape[0]
        D = feature.shape[1]
        # C=numpy.max(label)+1
        # C=C.astype(int)
        C = len(self.classes_)

        # transoform label into a 1-d array to avoid possible errors
        label = indices

        # make class label based on 1-of-K representation
        label_1ofK = zeros((N, C))
        for n in range(N):
            label_1ofK[n, label[n]] = 1

        # add a bias term to feature
        feature = hstack((feature, ones((N, 1))))
        D += 1

        # set initial values of theta (wieghts) and
        # alpha (relavence parameters)
        theta = zeros((D, C))
        alpha = ones((D, C))
        isEffective = ones((D, C))
        effectiveFeature = range(D)
        num_effectiveWeights = sum(isEffective)

        # Variational baysian method (see Yamashita et al., 2008)
        for iteration in range(self.max_iter):

            # theta-step
            newThetaParam = self.__thetaStep(
                theta, alpha, label_1ofK, feature, isEffective)
            theta = newThetaParam['mu']  # the posterior mean of theta
            if iteration == 0:
                funcValue_pre = newThetaParam['funcValue']
                funcValue = newThetaParam['funcValue']
            else:
                funcValue_pre = funcValue
                funcValue = newThetaParam['funcValue']

            # alpha-step
            alpha = self.__alphaStep(
                alpha, newThetaParam['mu'], newThetaParam['var'], isEffective)

            # pruning of irrelevant dimensions (that have large alpha values)
            isEffective = ones(theta.shape)
            isEffective[alpha > 1e+3] = 0
            theta[alpha > 1e+3] = 0

            dim_excluded = where(all(isEffective == 0, axis=1))
            theta = delete(theta, dim_excluded, axis=0)
            alpha = delete(alpha, dim_excluded, axis=0)
            feature = delete(feature, dim_excluded, axis=1)
            isEffective = delete(isEffective, dim_excluded, axis=0)
            effectiveFeature = delete(effectiveFeature, dim_excluded, axis=0)

            # show progress
            if self.verbose:
                if not num_effectiveWeights == sum(isEffective):
                    num_effectiveWeights = sum(isEffective)
                    print("# of iterations: %d,  # of effective dimensions: %d"
                          % (iteration + 1, len(effectiveFeature)))
                    print("# of iterations: %d,  FuncValue: %f"
                          % (iteration + 1, newThetaParam['funcValue']))
            if iteration > 1 and abs(funcValue - funcValue_pre) < self.tol:
                break

        temporal_theta = zeros((D, C))
        temporal_theta[effectiveFeature, :] = theta
        theta = temporal_theta

        self.coef_ = transpose(theta[:-1, :])
        self.intercept_ = theta[-1, :]
        return self

    def predict(self, feature):
        """predict(self, feature) method of SMLR instance

        Predict class labels for samples in feature (in the same way as
        logistic.py in sklearn).

        Parameters:
            feature: {array-like, sparse matrix},
                shape = [n_samples, n_features]
                Samples.

        Returns:
            C: array, shape = [n_samples]
                Predicted class label per sample.
        """

        # add a bias term to feature
        feature = hstack((feature, ones((feature.shape[0], 1))))

        # load weights
        w = vstack((transpose(self.coef_), self.intercept_))

        # predictive probability calculation
        p = exp(feature.dot(w))
        p /= p.sum(axis=1)[:, newaxis]
        predicted_label = self.classes_[argmax(p, axis=1)]
        return array(predicted_label)

    def decision_function(self, feature):
        # add a bias term to feature
        feature = hstack((feature, ones((feature.shape[0], 1))))

        # load weights
        w = vstack((transpose(self.coef_), self.intercept_))

        return feature.dot(w)

    def predict_proba(self, feature):
        """Probability estimates.

        The returned estimates for all classes are ordered by the
        label of classes (in the same way as logistic.py in sklearn).

        Parameters:
            feature: array-like, shape = [n_samples, n_features]

        Returns:
            T: array-like, shape = [n_samples, n_classes]
                Returns the probability of the sample for each class
                in the model, where classes are ordered as they are in
                ``self.classes_``.
        """

        # add a bias term to feature
        feature = hstack((feature, ones((feature.shape[0], 1))))

        # load weights
        w = vstack((transpose(self.coef_), self.intercept_))

        # predictive probability calculation
        p = exp(feature.dot(w))
        p /= p.sum(axis=1)[:, newaxis]
        return p

    def predict_log_proba(self, feature):
        """Log of probability estimates.

        The returned estimates for all classes are ordered by the
        label of classes (in the same way as logistic.py in sklearn).

        Parameters:
            feature: array-like, shape = [n_samples, n_features]

        Returns:
            T: array-like, shape = [n_samples, n_classes]
                Returns the log-probability of the sample for each class
                in the model, where classes are ordered as they are in
                ``self.classes_``.
        """
        p = self.predict_proba(feature)
        return log(p)

    def __thetaStep(self, theta, alpha, Y, X, isEffective):
        # chack # of dimensions, # of samples, and # of classes

        D = X.shape[1]
        C = Y.shape[1]

        # Take indices for effective features (if alpha > 10^3, that dimension is
        # ignored in the following optimization steps)
        FeatureNum_effectiveWeight = []
        ClassNum_effectiveWeight = []
        for c in range(C):
            for d in range(D):
                if isEffective[d, c] == 1:
                    FeatureNum_effectiveWeight.append(d)
                    ClassNum_effectiveWeight.append(c)

        # Declaration of subfunction. this function transform concatenated
        # effective weight paramters into the original shape
        def thetaConcatenated2thetaOriginalShape(theta_concatenated):
            if len(theta_concatenated) != len(FeatureNum_effectiveWeight):
                raise ValueError("The size of theta_concatenated is wrong")

            theta_original = zeros((D, C))
            for index_effective_weight in range(len(FeatureNum_effectiveWeight)):
                theta_original[
                    FeatureNum_effectiveWeight[index_effective_weight],
                    ClassNum_effectiveWeight[index_effective_weight]] =\
                    theta_concatenated[index_effective_weight]
            return theta_original

        # set the cost function that will be minimized in the following
        # optimization
        def func2minimize(theta_concatenated):
            theta_originalShape = thetaConcatenated2thetaOriginalShape(
                theta_concatenated)
            return -self.__funcE(theta_originalShape, alpha, Y, X)

        # set the gradient for Newton-CG based optimization
        def grad2minimize(theta_concatenated):
            theta_originalShape = thetaConcatenated2thetaOriginalShape(
                theta_concatenated)
            gradE_originalShape = self.__gradE(
                theta_originalShape, alpha, Y, X)

            # ignore the dimensions that have large alphas
            dim_ignored = isEffective.ravel(order='F')[:, newaxis]
            dim_ignored = nonzero(1 - dim_ignored)
            gradE_used = delete(gradE_originalShape, dim_ignored[0])
            return -gradE_used

        # set the Hessian for Newton-CG based optimization
        def Hess2minimize(theta_concatenated):
            theta_originalShape = thetaConcatenated2thetaOriginalShape(
                theta_concatenated)
            HessE_originalShape = self.__HessE(
                theta_originalShape, alpha, Y, X)

            # ignore the dimensions that have large alphas
            dim_ignored = isEffective.ravel(order='F')[:, newaxis]
            dim_ignored = nonzero(1 - dim_ignored)
            HessE_used = delete(HessE_originalShape, dim_ignored[0], axis=0)
            HessE_used = delete(HessE_used, dim_ignored[0], axis=1)
            return -HessE_used

        # set the initial value for optimization. we use the current theta for
        # this.
        x0 = theta.ravel(order='F')[:, newaxis]
        dim_ignored = isEffective.ravel(order='F')[:, newaxis]
        dim_ignored = nonzero(1 - dim_ignored)
        x0 = delete(x0, dim_ignored[0])

        # Optimization of theta (weight paramter) with scipy.optimize.minimize
        res = minimize(func2minimize, x0, method='Newton-CG',
                       jac=grad2minimize, hess=Hess2minimize, tol=1e-3)
        mu = thetaConcatenated2thetaOriginalShape(res['x'])

        # The covariance matrix of the posterior distribution
        cov = linalg.inv(Hess2minimize(res['x']))

        # The diagonal elements of the above covariance matrix
        var = diag(cov)
        var = thetaConcatenated2thetaOriginalShape(var)

        param = {'mu': mu, 'var': var, 'funcValue': res['fun']}
        return param

    def __alphaStep(self, alpha, theta, var, isEffective):
        D = alpha.shape[0]
        C = alpha.shape[1]
        for c in range(C):
            for d in range(D):
                if isEffective[d, c] == 1:
                    alpha[d, c] = (1 - alpha[d, c] * var[d, c]) / theta[d, c] ** 2
                else:
                    alpha[d, c] = 1e+8
        return alpha

    def __funcE(self, theta, alpha, Y, X):
        # theta: weights for classification, dimensions by # of classes
        # alpha: relavance parameters in ARD, dimensions by # of classes
        # Y: label matrix, 1-of-K representation, # of samples by # of classes
        # X: feature matrix, # of samples by # of dimensions
        # output: log likelihood function of theta (averaged over alpha)

        linearSum = X.dot(theta)
        fone = sum(Y * linearSum, axis=1) - \
               log(sum(exp(linearSum), axis=1))
        E = sum(fone) - (0.5) * sum(theta.ravel(order='F') *
                                    alpha.ravel(order='F') ** 2)
        return E

    def __gradE(self, theta, alpha, Y, X):
        # theta: weights for classification, dimensions by # of classes
        # alpha: relavance parameters in ARD, dimensions by # of classes
        # Y: label matrix, 1-of-K representation, # of samples by # of classes
        # X: feature matrix, # of samples by # of dimensions
        # output: The gragient of funcE. This is used for Q-step optimization.

        D = X.shape[1]
        C = Y.shape[1]

        dE = zeros((theta.shape[0] * theta.shape[1], 1))
        linearSumExponential = exp(X.dot(theta))
        p = linearSumExponential / sum(linearSumExponential, axis=1)[:, newaxis]

        for c in range(C):
            temporal_dE = sum(
                (Y[:, c] - p[:, c]) * X.T, axis=1)[:, newaxis]
            A = diag(alpha[:, c])
            temporal_dE -= transpose([dot(A, theta[:, c])])
            dE[c * D:((c + 1) * D), 0] = squeeze(temporal_dE)

        return squeeze(dE)

    def __HessE(self, theta, alpha, Y, X):
        # theta: weights for classification, dimensions by # of classes
        # alpha: relavance parameters in ARD, dimensions by # of classes
        # Y: label matrix, 1-of-K representation, # of samples by # of classes
        # X: feature matrix, # of samples by # of dimensions
        # output: The Hessian of funcE. This is used for Q-step optimization.

        N = X.shape[0]
        D = X.shape[1]
        C = Y.shape[1]

        linearSumExponential = exp(X.dot(theta))
        p = linearSumExponential / sum(
            linearSumExponential, axis=1)[:, newaxis]
        H = zeros((C * D, C * D))

        for n in range(N):
            M1 = diag(p[n, :])
            M2 = dot(transpose([p[n, :]]), [p[n, :]])
            M3 = dot(transpose([X[n, :]]), [X[n, :]])
            H = H - kron(M1 - M2, M3)
        H = H - diag(alpha.ravel(order='F'))
        # Derivation came from Yamashita et al., Nuroimage,2008., but
        # exactly speaking, the last term is modified.
        # The above is consistent with SLR toolbox (MATLAB-based implementation by
        # Yamashita-san) rather than the paper.
        return H


if __name__ == '__main__':
    ''' demo '''


    def demo_data():
        # Num of samples
        N = 100
        # Label vector
        label4training = vstack((zeros((N, 1)), ones((N, 1))))
        label4test = vstack((zeros((N, 1)), ones((N, 1))))
        # Featuret
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
        X, y = feature4training, label4training
        TestX, Testy = feature4test, label4test
        return X, y, TestX, Testy


    X, y, TestX, Testy = demo_data()
    # Prepare classifier objects
    smlr = SMLR(max_iter=1000, tol=1e-5, verbose=1)
    print("SMLR learning")
    smlr.fit(X, y)
    print("The SLMR weights obtained")
    print(transpose(smlr.coef_))  # 最后一位对应常数项

    # Linear boundary in the feature space
    for n in range(len(X)):
        if y[n] == 0:
            plt.scatter(X[n, 0], X[n, 1], color='r')
        else:
            plt.scatter(X[n, 0], X[n, 1], color='b')
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    w = smlr.coef_[0, :]
    x = np.arange(-5, 5, 0.001)
    y = (-w[-1] - x * w[0]) / w[1]
    plt.plot(x, y, color='black')
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.grid()
    plt.show()

    # generalization test
    PredsLabel = smlr.predict(TestX)
    cnt_correct = 0
    for i in range(len(Testy)):
        if Testy[i] == PredsLabel[i]:
            cnt_correct += 1
    accuracy = np.double(cnt_correct) / len(Testy) * 100
    print("SMLR accuracy: %s" % (accuracy))

