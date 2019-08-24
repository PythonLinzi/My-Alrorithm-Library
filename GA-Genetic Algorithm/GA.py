import numpy as np
from numpy.random import rand, randint
from numpy.random import choice
from numpy import arange, log2
from numpy import argmax, argmin
from numpy import max, min
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
        self.bnds = bnd # 取值范围
        self.tol = tol # 精度 precision
        self.lb = bnd[0]
        self.rb = bnd[1]
        u_b = bnd[1] - bnd[0]
        self.Dna_Len = int(log2(u_b / tol)) + 1
        self.pop = randint(0,2,size=(self.size, self.Dna_Len))
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
        return pop.dot(self.dot2) / float(2 ** self.Dna_Len) * self.bnds[1]

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
        :param ch: child DNA
        :return: new child
        '''
        for point in range(0, self.Dna_Len):
            if rand() < self.mr:
                ch[point] = 1 if ch[point] == 0 else 0
        return ch

    def compute(self, niter=100):
        '''
        Main Computing Loop
        :param niter: int, number of iterations
                    number of generation
        :return: best X, and best y
        '''
        bestX = self.__Bin2Dec(self.pop[0])
        bestY = self.f(bestX)
        t4plot = [0]
        y4plot = [bestY]
        tx, ty = bestX, bestY
        for i in range(niter):
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
            t4plot.append(i + 1)
            y4plot.append(bestY)
        s1 = "Global Minimum: xmin = {0}, "
        s2 = "f(xmin) = {1:.6f}"
        tmps = s1 + s2
        print(tmps.format(bestX, bestY))
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
    def f(x):
        ret = (x - 2) * (x + 3) * (x + 8) * (x - 9)
        return ret


    ga = GA(f=f, ps=50, cr=0.8, mr=0.005, bnd=[-10, 10], tol=1e-3)
    bestX, bestY = ga.compute(niter=200)

