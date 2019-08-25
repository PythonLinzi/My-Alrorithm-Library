import numpy as np
from numpy.random import rand, randint
from numpy.random import choice
from numpy import arange, log2, dot
from numpy import argmin, array
from numpy import ndarray, floor
import matplotlib.pyplot as plt


class GA():
    '''genetic algorithm'''
    def __init__(self, f, ps, cr, mr, bnd, tol, D, isInt):
        '''
        :param f: Target Function
        :param ps: int, population size
        :param cr: cross_rate
        :param mr: mutate_rate
        :param bnd: np.ndarray, bounds
        :param tol: tolerance
        :param D: int, dimensions of vars
        :param isInt: list, indecies of vars which is integer
        '''
        self.f = f
        self.size = ps
        self.cr = cr
        self.mr = mr
        self.bnd = bnd # 取值范围
        self.tol = tol # 精度 precision
        self.D = D
        self.isInt = isInt
        self.lb = bnd[:, 0]
        self.ub = bnd[:, 1]
        self.u_b = self.ub - self.lb
        tmp = log2(self.u_b / tol) + 1
        self.Dna_Len = []
        for l in tmp:
            self.Dna_Len.append(int(l))
        n, m = self.size, self.Dna_Len
        self.pop = self.__PopInit(n, D, m)
        self.dot2 = []
        for l in self.Dna_Len:
            dot2 = 2 ** arange(l)[::-1]
            self.dot2.append(dot2)
        self.dot2 = array(self.dot2)

    def __PopInit(self, n, D, m):
        '''
        Population Initialize
        :param n: int, size of Pop
        :param D: int, dimensions
        :param m: list, [d1, d2, ...(dna_len)]
        :return: ndarray, pop
        '''
        pop = []
        for i in range(n):
            ind = []
            for j in range(D):
                tmp = randint(0, 2, m[j])
                ind.append(tmp)
            pop.append(ind)
        return array(pop)

    def __func(self, X:ndarray):
        y = []
        for x in X:
            y.append(self.f(x))
        return array(y)

    def __fitness(self, y):
        '''
        Fitness Function for Minimal Problem
        :param y: target y
        :return: Fitness
        '''
        return max(y) - y + 1e-3

    def __B2D(self, ind):
        '''
        Convert individual DNA from Binary to Decimal
        :param ind: individual
        :return: np.ndarray
        '''
        ret, M = [], []
        for l in self.Dna_Len:
            M.append(float(2 ** l))
        for j in range(self.D):
            x = dot(ind[j], self.dot2[j]) / M[j] * self.u_b[j]
            x += self.lb[j]
            if self.isInt[j]:
                ret.append(floor(x))
            else:
                ret.append(x)
        return array(ret)

    def __Bin2Dec(self, pop):
        '''
        Convert pop's DNA from Bin to Dec
        :param pop: np.ndarray, pop's DNA in Bin
        :return: np.ndarray, pop's decimal
        '''
        ret = []
        for i, p in enumerate(pop):
            tmp = self.__B2D(p)
            ret.append(tmp)
        return array(ret)

    def __select(self, fitness):
        ''' nature selection '''
        w = fitness / fitness.sum()
        s = self.size
        idx = choice(arange(s), size=s, p=w)
        return self.pop[idx]

    def __cross(self, pa:ndarray, pop: ndarray):
        '''
        mating process (genes crossover)
        :param pa: np.ndarry, parent DNA
        :param pop: np.ndarry, population
        :return pa: np.ndarry, new child
        '''
        n, D = self.size, self.D
        m = self.Dna_Len
        if rand() < self.cr:
            idx = randint(0, n, size=1)
            pa_ = np.reshape(pop[idx], pa.shape)
            #pa_ = np.reshape(pop[idx], (D, m[j]))
            for j in range(D):
                c_idx = randint(0, 2, size=m[j]).astype(np.bool)
                pa[j][c_idx] = pa_[j][c_idx]
        return pa

    def __mutate(self, ch):
        '''
        :param ch: child DNA
        :return: new child
        '''
        m = self.Dna_Len
        D = self.D
        for i in range(D):
            for j in range(m[i]):
                if rand() < self.mr:
                    ch[i][j] = 1 if ch[i][j] == 0 else 0
        return ch

    def compute(self, niter=100, plot=True):
        '''
        Main Computing Loop
        :param niter: int, number of iterations
                    number of generation
        :return: best X, and best y
        '''
        bestX = self.__B2D(self.pop[0])
        bestY = self.f(bestX)
        t4plot = [0]
        y4plot = [bestY]
        tx, ty = bestX, bestY

        ss = 'iter = {0},  y = {1}'
        for i in range(niter):
            print(ss.format(i + 1, bestY))
            X = self.__Bin2Dec(self.pop)
            Y = self.__func(X)
            fit = self.__fitness(Y)
            tx = X[argmin(Y)]
            ty = min(Y)
            self.pop = self.__select(fit)
            pop = self.pop.copy()
            for pa in self.pop:
                ch = self.__cross(pa, pop)
                ch = self.__mutate(ch)
                pa = ch
            if ty < bestY:
                bestX, bestY = tx, ty
            t4plot.append(i + 1)
            y4plot.append(bestY)
        s1 = "Global Minimum: xmin = {0}, "
        s2 = "f(xmin) = {1:.6f}"
        tmps = s1 + s2
        print(tmps.format(bestX, bestY))
        if plot == True:
            self.__conver_plot(t4plot, y4plot)

        return bestX, bestY

    def __conver_plot(self, x, y):
        '''
        Convergence Process Plotting
        :param x: list, X
        :param y: list, y
        :return:
        '''
        plt.scatter(x, y, marker='*', s=10)
        plt.grid()
        plt.title('Convergence Process')
        plt.xlabel('X')
        plt.ylabel('y')
        plt.show()


if __name__ == '__main__':
    def target(x:ndarray):
        ret = x[0] ** 2 + x[1] ** 2 + 3 * x[2] ** 2 + 4 * x[3] ** 2 + 2 * x[4] ** 2 \
              - 8 * x[0] - 2 * x[1] - 3 * x[2] - x[3] - 2 * x[4]
        return -ret

    def bounds(x:ndarray):
        bnds = []
        bnds.append(x.sum() - 400)
        bnds.append(x[0] + 2 * x[1] + 2 * x[2] + x[3] + 6 * x[4] - 800)
        bnds.append(2 * x[0] + x[1] + 6 * x[2] - 200)
        bnds.append(x[2] + x[3] + 5 * x[4] - 200)
        return array(bnds)


    def f(x:ndarray):
        y = target(x)
        penalty = 1e30
        bnds = bounds(x)
        for bnd in bnds:
            if bnd > 0:
                y += (penalty * bnd)
        return y

    isInt = [True] * 5
    bnds = array([[0, 60], [95, 100], [0, 1], [95, 100], [10, 30]])
    ga = GA(f=f, ps=50, cr=0.8, mr=0.3, bnd=bnds, tol=1e-2, D=5, isInt=isInt)
    bestX, bestY = ga.compute(niter=500, plot=True)

    acc = 100 * bestY / -51568
    if np.all(bounds(bestX) <= 0):
        print("满足约束条件!")
    print('Accuracy = {0}%'.format(acc))
    #print(f(array([50, 99, 0, 99, 20])))

'''
Global Minimum: xmin = [50. 98.  0. 99. 19.], f(xmin) = -51297.000000
满足约束条件!
Accuracy = 99.47448029785913%
'''
