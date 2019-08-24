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
    penelty = np.inf # 惩罚系数
    for value in bnds:
        if value > 0: # violation of constrains
            y += (penelty * value)
    return y


def PSO(N=50, niter=100, bnds=[-10, 10]):
    w, c1, c2 = 1, 2, 2.1
    vmin, vmax = -1, 1
    c = c1 + c2
    K = 2 / (np.abs(2 - c - np.sqrt(c * c - 4 * c)))
    x, v = bnds[0] + (bnds[1] - bnds[0]) * rand(N), rand(N)
    y = np.array([f(v) for v in x])
    pb_x, pb_y = x.copy(), y.copy()
    gb_x, gb_y = x[y.argmin()], y.min()
    GroupTime, GroupBest = [], [] # for plotting
    for _ in range(niter):
        for i in range(N):
            pb = c1 * rand() * (pb_x[i] - x[i])
            gb = c2 * rand() * (gb_x - x[i])
            v[i] = K * (v[i] + pb + gb)
            v[i] = min(v[i], vmax)
            x[i] += max(v[i], vmin)
            y[i] = f(x[i])
            if y[i] < pb_y[i]:
                pb_x[i], pb_y[i] = x[i], y[i]
            if y[i] < gb_y:
                gbest_x, gb_y = x[i], y[i]
        GroupTime.append(_ + 1)
        GroupBest.append(gb_y)
    s1 = "Global Minimum: xmin = {0}, "
    s2 = "f(xmin) = {1:.6f}"
    ss = s1 + s2
    print(ss.format(gb_x, gb_y))
    return [gb_x, gb_y], GroupTime, GroupBest

from datetime import datetime
s = datetime.now()
res, gt, gy = PSO()
e = datetime.now()
print("Running Time:", e - s)
import matplotlib.pyplot as plt
plt.plot(gt, gy, label='finding process', c='r')
plt.scatter(gt, gy, label='finding process', s=10)
plt.xlabel('Iteration Time')
plt.ylabel('Target')
plt.title('Convergence')
plt.grid()
plt.show()


'''
Global Minimum: xmin = 6.484184871679452, f(xmin) = -1549.730940
Running Time: 0:00:00.079901
'''
