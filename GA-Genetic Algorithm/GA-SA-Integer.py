import numpy as np
from numpy import exp, log2, array, arange
from numpy.random import rand, randint, choice
from numpy import argmin, dot, zeros
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
        Mutation Process
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

    def compute(self, niter=100, bf=None):
        '''
        Main Computing Loop
        :param niter: int, number of iterations
        :param bf: Boundary Function
        :return: best X, best y, t4plot, y4plot
        '''
        bestX = self.__B2D(self.pop[0])
        bestY = self.f(bestX)
        t4plot = []
        y4plot = []
        tx, ty = bestX, bestY
        ss = 'iter = {0},  y = {1}'
        for i in range(niter):
            #print(ss.format(i + 1, bestY))
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
        return bestX, bestY, t4plot, y4plot


class SA:
    ''' Simulated Annealing '''
    def __init__(self, f, niter=100, T=1e3, fT=1, ac=0.9, D=1):
        '''
        Params Initialize
        :param f: Target Funcion(Min)
        :param niter: int, number of iterations
        :param T: float, initial temperature
        :param fT: float, final temperature
        :param ac: float, attenuation coefficient
        :param D: int, dimensions of vars
        '''
        self.f = f
        self.niter = niter
        self.T = T
        self.fT = fT
        self.ac = ac
        self.D = D
        self.x0 = rand(D)
        self.K = 1
        self.step = 1

    def set_x0(self, x0):
        '''
        Set init x
        :param x0: init guess
        :return: None
        '''
        self.x0 = x0

    def set_K(self, k):
        '''
        Coeff K's setting
        :param k: coef
        :return: None
        '''
        self.K = k

    def set_step(self, step):
        '''
        Step Setting
        :param step: step
        :return: None
        '''
        self.step = step

    def compute(self):
        f = self.f
        niter = self.niter
        T, ft = self.T, self.fT
        ac = self.ac
        D = self.D
        x = self.x0
        y = f(x)
        ret_X = self.x0
        ret_Y = self.f(x)
        K = self.K
        step = self.step
        sche = "niter = {0}, y = {1}"
        cnt = 0
        t4plot = []
        y4plot = []
        while T > ft:
            for i in range(niter):
                cnt += 1
                if cnt % 100 == 0:
                    t4plot.append(cnt / 100)
                    y4plot.append(ret_Y)
                    #print(sche.format(cnt, ret_Y))
                y, ret_Y = f(x), f(ret_X)
                new_X = x + step * randint(-1, 2, D)
                new_Y = f(new_X)
                dy1 = new_Y - y
                dy2 = new_Y - ret_Y
                if dy1 < 0:
                    x = new_X
                    y = new_Y
                elif exp(-dy1 / (K * T)) > rand():
                    x = new_X
                    y = new_Y
                if dy2 < 0:
                    ret_X = new_X
                    ret_Y = new_Y
            T *= ac
        s1 = "Global Minimum: xmin = {0}, "
        s2 = "f(xmin) = {1:.6f}"
        ss = s1 + s2
        print(ss.format(ret_X, ret_Y))
        return ret_X, ret_Y, t4plot, y4plot


class GSA:
    ''' GA -> SA -> result'''
    def __init__(self, func, bnd, n1=100, n2=500, D=1):
        '''
        :param fun: target function(min)
        :param bnd: ndarray, bounds of vars
        :param n1: int, niter of GA
        :param n2: int, niter of SA
        '''
        self.f = func
        self.n1 = n1
        self.n2 = n2
        self.bnd = bnd
        self.ps = 50
        self.cr = 0.8
        self.mr = 0.1
        self.tol = 1e-2
        self.D = D
        self.isInt = zeros(D).astype(np.bool)
        self.T = 1e3
        self.fT = 1
        self.ac = 0.9

    def ga_set(self, ps, cr, mr, bnd, tol, isInt):
        '''
        Genetic Algorithm Setting
        :param ps: int, population size
        :param cr: cross_rate
        :param mr: mutate_rate
        :param bnd: np.ndarray, bounds
        :param tol: tolerance
        :param D: int, dimensions of vars
        :param isInt: list, indecies of vars which is integer
        :return: None
        '''
        self.ps = ps
        self.cr = cr
        self.mr = mr
        self.bnd = bnd
        self.tol = tol
        self.isInt = isInt

    def sa_set(self, niter=100, T=1e3, fT=1, ac=0.9):
        '''
        Params Initialize
        :param niter: int, number of iterations
        :param T: float, initial temperature
        :param fT: float, final temperature
        :param ac: float, attenuation coefficient
        :param D: int, dimensions of vars
        '''
        self.n2 = niter
        self.T = T
        self.fT = fT
        self.ac = ac

    def __conver_plot(self, t1, y1, t2, y2):
        '''
        Convergence Process Plotting
        :param x: list, X
        :param y: list, y
        :return:
        '''
        n2 = len(y2)
        for i in range(n2 - 1, -1, -1):
            t2[i] += t1[-1]
        gl = 'GA(niter/1)'
        sl = 'SA(niter/100)'
        plt.scatter(t1, y1, marker='*', s=10, label=gl)
        plt.scatter(t2, y2, marker='*', s=10, label=sl)
        plt.legend()
        plt.grid()
        plt.title('Convergence Process')
        plt.xlabel('niter')
        plt.ylabel('y')
        plt.show()

    def compute(self, plot=True, bf=None):
        f = self.f
        n1 = self.n1
        n2 = self.n2
        bnd = self.bnd
        ps = self.ps
        cr = self.cr
        mr = self.mr = 0.1
        tol = self.tol
        D = self.D
        isInt = self.isInt
        T = self.T
        fT = self.fT
        ac = self.ac
        ga = GA(f, ps, cr, mr, bnd, tol, D, isInt)
        sa = SA(f, n2, T, fT, ac, D)
        print("----- GA -----")
        x0, y0, tp1, yp1 = ga.compute(niter=n1, bf=bf)
        sa.set_x0(x0=x0)
        print("----- SA -----")
        ret_x, ret_y, tp2, yp2 = sa.compute()
        if plot == True:
            self.__conver_plot(tp1, yp1, tp2, yp2)
        return ret_x, ret_y



if __name__ == '__main__':
    def target(x:ndarray):
        ret = x[0] ** 2 + x[1] ** 2 + 3 * x[2] ** 2 + 4 * x[3] ** 2 + 2 * x[4] ** 2 \
              - 8 * x[0] - 2 * x[1] - 3 * x[2] - x[3] - 2 * x[4]
        return -ret

    bnds = array([[0, 60], [95, 99], [0, 1], [95, 99], [10, 30]])
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

    def f(x:ndarray):
        y = target(x)
        penalty = 1e30
        cons = constraints(x)
        for bnd in cons:
            if bnd > 0:
                y += (penalty * bnd)
        return y


    bnd_ga = array([[0, 61], [95, 100], [0, 2], [95, 100], [10, 31]])
    isInt = [True] * 5
    gsa = GSA(func=f, bnd=bnds, n1=150, n2=200, D=5)
    gsa.ga_set(ps=30, cr=0.8, mr=0.1, bnd=bnds, tol=1e-2, isInt=isInt)
    x, y = gsa.compute(bf=constraints)
    if np.all(constraints(x) <= 0):
        print("满足约束!")

