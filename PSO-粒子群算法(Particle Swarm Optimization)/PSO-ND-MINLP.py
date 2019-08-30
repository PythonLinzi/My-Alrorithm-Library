'''
MILNP: Mixed Integer Nonlinear Programming
Particle Swarm Optimization Algorithm
Pay attention to adjusting Parameters
Parameters:
    size: 种群个体数量(一般取20~50 or 100~200), niter: 迭代次数
    vmin, vmax: 最大最小速度--限定步长
    w: 惯性因子(>=0)
    c1, c2: 学习因子(通常c1=c2=2)
    K: 收敛因子(保证收敛性, 通常令c1+c2=4.1, s.t. K=0.729)
'''

import numpy as np
from numpy import ndarray, array, abs
from numpy import sqrt, append
from numpy.random import rand, randint
import matplotlib.pyplot as plt


class PSO:
    ''' Particle Swarm Optimization '''
    def __init__(self, func, bnds, cons, isInt, D=5):
        '''
        Initialization
        :param func: Target Function(Min)
        :param bnds: ndarray, Bounds of Vars
        :param cons: Constraints Function, CF(x) <= 0
        :param isInt: ndarray, array([bool])
        :param D: int, dimensions of vars
        '''
        self.func = func
        self.bnds = bnds
        self.cons = cons
        self.size = 20
        self.isInt = isInt
        self.D = D
        self.vrange = [-1, 1]
        self.w = 1
        self.c1 = 2
        self.c2 = 2.1
        self.c = self.c1 + self.c2
        c = self.c
        self.K = 2 / (abs(2 - c - sqrt(c * c - 4 * c)))
        self.tol = 1e-4

    def __f(self, x:ndarray):
        inf = 1e99
        ret = self.func(x)
        cons = self.cons(x)
        m = self.D
        bnds = self.bnds
        for j in range(m):
            cons = append(cons, bnds[j][0] - x[j])
            cons = append(cons, x[j] - bnds[j][1])
        for con in cons:
            if con > 0:
                ret += (inf * con)
        return ret

    def __PopInit(self):
        n = self.size
        m = self.D
        bnds = self.bnds
        isInt = self.isInt
        x = array([])
        for i in range(self.size):
            xi = array([])
            for j in range(m):
                l, u = bnds[j]
                if isInt[j] == True:
                    xij = randint(l, u + 1)
                else:
                    xij = (u - l) * rand() + l
                xi = append(xi, xij)
            x = append(x, xi)
        return x.reshape(n, m)

    def __VInit(self):
        l, u = self.vrange
        v = (u - l) * rand(self.size, self.D) + l
        return v

    def __sign(self, v):
        if v > 0:
            return 1
        elif v < 0:
            return -1
        if rand() > 2 / 3:
            return 1
        elif rand() < 1 / 3:
            return -1
        else:
            return 0

    def __Cons_Check(self, x:ndarray):
        cons = self.cons(x)
        if np.all(cons <= self.tol):
            print("满足约束！")
            return True
        else:
            print(cons)
            return False

    def __set_tol(self, tol):
        self.tol = tol

    def set_PopSize(self, size=20):
        self.size = size

    def __conver_plot(self, t, y):
        '''
        Convergence Process Plotting
        :param t: list, t
        :param y: list, y
        :return:
        '''
        plt.scatter(t, y, marker='*', s=10, c='r')
        plt.plot(t, y, linewidth=1)
        plt.grid()
        plt.title('Convergence Process')
        plt.xlabel('niter')
        plt.ylabel('y')
        plt.show()

    def compute(self, niter=200, tol=1e-4, plot=False):
        f = self.__f
        c1 = self.c1
        c2 = self.c2
        vmin, vmax = self.vrange
        K = self.K
        x = self.__PopInit()
        v = self.__VInit()
        y = np.array([f(x_) for x_ in x])
        px, py = x.copy(), y.copy()
        gx, gy = x[y.argmin()], y.min()
        t4plot = []
        y4plot = []
        for _ in range(niter):
            for i in range(self.size):
                for j in range(self.D):
                    pb = c1 * rand(1) * (px[i][j] - x[i][j])
                    gb = c2 * rand(1) * (gx[j] - x[i][j])
                    v[i][j] = K * (v[i][j] + pb + gb)
                    v[i][j] = min(v[i][j], vmax)
                    v[i][j] = max(v[i][j], vmin)
                    x[i][j] += self.__sign(v[i][j])
                y[i] = f(x[i])
                if y[i] < py[i]:
                    px[i], py[i] = x[i], y[i]
                if y[i] < gy:
                    gx, gy = x[i], y[i]
            t4plot.append(_ + 1)
            y4plot.append(gy)
        s1 = "Global Minimum: xmin = {0}, "
        s2 = "f(xmin) = {1:.6f}"
        ss = s1 + s2
        print(ss.format(gx, gy))
        self.__set_tol(tol=tol)
        self.__Cons_Check(gx)
        if plot == True:
            self.__conver_plot(t4plot, y4plot)
        return gx, gy



if __name__ == '__main__':
    def func(x:ndarray):
        ret = x[0] ** 2 + x[1] ** 2 + 3 * x[2] ** 2 + 4 * x[3] ** 2 + 2 * x[4] ** 2 \
              - 8 * x[0] - 2 * x[1] - 3 * x[2] - x[3] - 2 * x[4]
        return -ret


    def constraints(x:ndarray):
        cons = []
        cons.append(x.sum() - 400)
        cons.append(x[0] + 2 * x[1] + 2 * x[2] + x[3] + 6 * x[4] - 800)
        cons.append(2 * x[0] + x[1] + 6 * x[2] - 200)
        cons.append(x[2] + x[3] + 5 * x[4] - 200)
        for i in range(len(bnds)):
            cons.append(x[i] - bnds[i][1])
            cons.append(bnds[i][0] - x[i])
        return array(cons)


    bnds = array([[0, 60], [95, 99], [0, 1], [95, 99], [10, 30]])
    isInt = array([True, True, True, True, True])
    pso = PSO(func=func, bnds=bnds, cons=constraints, isInt=isInt, D=5)
    pso.set_PopSize(size=20)
    pso.compute(niter=100, tol=1e-3, plot=True)



'''
Global Minimum: xmin = [50. 99.  0. 99. 20.], f(xmin) = -51568.000000
满足约束！
'''
