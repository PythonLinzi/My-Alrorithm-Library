'''
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
from numpy.random import rand
import matplotlib.pyplot as plt


class PSO:
    ''' Particle Swarm Optimization '''
    def __init__(self, func, bnds, cons, D=5):
        '''
        Initialization
        :param func: Target Function(Min)
        :param bnds: ndarray, Bounds of Vars
        :param cons: Constraints Function, CF(x) <= 0
        :param D: int, dimensions of vars
        '''
        self.func = func
        self.bnds = bnds
        self.cons = cons
        self.size = 20
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
        x = array([])
        for i in range(self.size):
            xi = array([])
            for j in range(m):
                lb, ub = bnds[j]
                xij = (ub - lb) * rand() + lb
                xi = append(xi, xij)
            x = append(x, xi)
        return x.reshape(n, m)

    def __VInit(self):
        l, u = self.vrange
        v = (u - l) * rand(self.size, self.D) + l
        return v

    def __Cons_Check(self, x:ndarray):
        cons = self.cons(x)
        if np.all(cons <= self.tol):
            print("满足约束！")
        else:
            print(cons)

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
                x[i] += v[i]
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
    def func(x: np.ndarray):
        return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8


    def constraints(x: np.ndarray) -> np.ndarray:
        ''' constrains <= 0 '''
        ans = array([-xx for xx in x])  # -X <= 0
        # -x1^2 + x2 - x3^2 <= 0
        con = -x[0] * x[0] + x[1] - x[2] * x[2]
        ans = append(ans, con)
        # x1 + x2^2 + x3^2 - 20 <= 0
        con = x[0] + x[1] * x[1] + x[2] * x[2] - 20
        ans = append(ans, con)
        # -x1 - x2^2 + 2 <= 0
        con = -x[0] - x[1] * x[1] + 2
        ans = append(ans, con)
        # -x2 - 2 * x3^2 + 3 <= 0
        con = -x[1] - 2 * x[2] * x[2] + 3
        ans = append(ans, con)
        return ans


    bnds = array([[0, 1], [0, 3], [0, 3]])
    pso = PSO(func=func, bnds=bnds, cons=constraints, D=3)
    pso.set_PopSize(size=20)
    pso.compute(niter=200, tol=1e-4, plot=True)



'''
Global Minimum: xmin = [0.55216734 1.20325918 0.94782404], f(xmin) = 10.651092
Running Time: 0:00:01.557554
'''
