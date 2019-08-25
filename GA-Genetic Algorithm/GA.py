import numpy as np
from numpy.random import rand, randint
from numpy.random import choice
from numpy import arange, log2
from numpy import argmin
import matplotlib.pyplot as plt


class GA():
    '''genetic algorithm'''
    def __init__(self, f, ps, cr, mr, bnd, tol):
        '''
        :param f: Target Function
        :param ps: int, population size
        :param cr: cross_rate
        :param mr: mutate_rate
        :param bnd: bounds
        :param tol: tolerance
        '''
        self.f = f
        self.size = ps
        self.cr = cr
        self.mr = mr
        self.bnd = bnd # 取值范围
        self.tol = tol # 精度 precision
        self.lb = bnd[0]
        self.ub = bnd[1]
        self.u_b = bnd[1] - bnd[0]
        self.Dna_Len = int(log2(self.u_b / tol)) + 1
        n, m = self.size, self.Dna_Len
        self.pop = randint(0,2,size=(n, m))
        self.dot2 = 2 ** arange(self.Dna_Len)[::-1]

    def __fitness(self, y):
        '''
        Fitness Function for Minimal Problem
        :param y: target y
        :return: Fitness
        '''
        return max(y) - y + 1e-3

    def __Bin2Dec(self, pop):
        '''convert binary DNA to decimal and normalize it to a range(xbound)'''
        M = float(2 ** self.Dna_Len)
        ret = pop.dot(self.dot2) / M * self.u_b
        ret += self.lb
        return ret

    def __select(self, fitness):
        ''' nature selection '''
        w = fitness / fitness.sum()
        s = self.size
        idx = choice(arange(s), size=s, p=w)
        return self.pop[idx]

    def __cross(self, pa, pop):
        '''
        mating process (genes crossover)
        :param pa: parent DNA
        :param pop: population
        :return:
        '''
        if rand() < self.cr:
            idx = randint(0, self.size, size=1)
            cross_idx = randint(0, 2, size=self.Dna_Len).astype(np.bool)
            pa[cross_idx] = pop[idx, cross_idx]
        return pa

    def __mutate(self, ch):
        '''
        Mutation Process
        :param ch: child DNA
        :return: new child
        '''
        for point in range(0, self.Dna_Len):
            if rand() < self.mr:
                ch[point] = 1 if ch[point] == 0 else 0
        return ch

    def compute(self, niter=100, plot=True, bf=None):
        '''
        Main Computing Loop
        :param niter: int, number of iterations
        :param bf: Boundary Function
        :return: best X, and best y
        '''
        bestX = self.__Bin2Dec(self.pop[0])
        bestY = self.f(bestX)
        t4plot = []
        y4plot = []
        tx, ty = bestX, bestY
        ss = 'iter = {0},  y = {1}'
        for i in range(niter):
            print(ss.format(i + 1, bestY))
            X = self.__Bin2Dec(self.pop)
            Y = self.f(X)
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
            if bf:
                if np.all(bf(bestX) <= 0):
                    t4plot.append(i + 1)
                    y4plot.append(bestY)
            else:
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
        plt.xlabel('niter')
        plt.ylabel('y')
        plt.show()


if __name__ == '__main__':
    def f(x):
        ret = (x - 2) * (x + 3) * (x + 8) * (x - 9)
        return ret


    ga = GA(f=f, ps=50, cr=0.8, mr=0.005, bnd=[-10, 10], tol=1e-3)
    bestX, bestY = ga.compute(niter=200)

