'''
Particle Swarm Optimization Algorithm
Pay attention to adjusting Parameters
Parameters:
    N: 种群个体数量(一般取20~50 or 100~200), niter: 迭代次数
    vmin, vmax: 最大最小速度--限定步长
    w: 惯性因子(>=0)
    c1, c2: 学习因子(通常c1=c2=2)
    K: 收敛因子(保证收敛性, 通常令c1+c2=4.1, s.t. K=0.729)
'''
import numpy as np
from numpy import exp
from numpy.random import rand


def target_func(x):
    return (x - 2) * (x + 3) * (x + 8) * (x - 9)

def Bounds(x):
    ''' constrains <= 0  '''
    bnds = [x - 10, -x - 10] # x - 10 <= 0; -x - 10 <= 0
    return np.array(bnds)

def f(x):
    y, bnds = target_func(x), Bounds(x)
    penelty = 0x3f3f3f3f # 注意适当调整惩罚系数
    for value in bnds:
        if value > 0: # violation of constrains
            y += (penelty * value)
    return y


def PSO():
    N, niter = 50, 500
    vmin, vmax = -1, 1
    w, c1, c2 = 1, 2, 2.1
    c = c1 + c2
    K = 2 / (np.abs(2 - c - np.sqrt(c * c - 4 * c)))
    bnds = [-10, 10]
    x, v = bnds[0] + (bnds[1] - bnds[0]) * rand(N), rand(N)
    y = np.array([f(v) for v in x])
    pbest_x, pbest_y = x.copy(), y.copy()
    gbest_x, gbest_y = x[y.argmin()], y.min()
    for _ in range(niter):
        for i in range(N):
            v[i] = K * (v[i] + c1 * rand(1) * (pbest_x[i] - x[i]) + c2 * rand(1) * (gbest_x - x[i]))
            v[i] = min(v[i], vmax)
            x[i] += max(v[i], vmin)
            y[i] = f(x[i])
            if y[i] < pbest_y[i]:
                pbest_x[i], pbest_y[i] = x[i], y[i]
            if y[i] < gbest_y:
                gbest_x, gbest_y = x[i], y[i]
    print("Global Minimum: xmin = {0}, f(xmin) = {1:.6f}".format(gbest_x, gbest_y))
    return gbest_x, gbest_y

from datetime import datetime
s = datetime.now()
PSO()
e = datetime.now()
print("Running Time:", e - s)


'''
Global Minimum: xmin = 6.484184832213667, f(xmin) = -1549.730940
Running Time: 0:00:00.473265
'''
