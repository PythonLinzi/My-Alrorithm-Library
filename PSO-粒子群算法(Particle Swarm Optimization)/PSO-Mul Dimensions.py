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


def target_func(x:np.ndarray):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8

def Bounds(x:np.ndarray) -> np.ndarray:
    ''' constrains <= 0 '''
    ans = [-xx for xx in x] # -X <= 0
    ans.append(-x[0] * x[0] + x[1] - x[2] * x[2]) # -x1^2 + x2 - x3^2 <= 0
    ans.append(x[0] + x[1] * x[1] + x[2] * x[2] - 20) # x1 + x2^2 + x3^2 - 20 <= 0
    ans.append(-x[0] - x[1] * x[1] + 2) # -x1 - x2^2 + 2 <= 0
    ans.append(-x[1] - 2 * x[2] * x[2] + 3) # -x2 - 2 * x3^2 + 3 <= 0
    return np.array(ans)

def f(x:np.ndarray):
    y, bnds = target_func(x), Bounds(x)
    penelty = np.inf
    for value in bnds:
        if value > 0: # violation of constrains
            y += (penelty * value)
    return y


def PSO(dimensions=3):
    '''
    Particle Swarm Optimization
    :param dimensions: int
    :return:
    '''
    n = dimensions # dimensions 维数
    N, niter = 20, 200
    vmin, vmax = -1, 1
    w, c1, c2 = 1, 2, 2.1
    c = c1 + c2
    K = 2 / (np.abs(2 - c - np.sqrt(c * c - 4 * c)))
    x, v = rand(N, n), rand(N, n) # 注意初始值X要在取值范围内随机投点
    y = np.array([f(v) for v in x])
    pbest_x, pbest_y = x.copy(), y.copy()
    gbest_x, gbest_y = x[y.argmin()], y.min()
    for _ in range(niter):
        for i in range(N):
            for j in range(n):
                pb = c1 * rand(1) * (pbest_x[i][j] - x[i][j])
                gb = c2 * rand(1) * (gbest_x[j] - x[i][j])
                v[i][j] = K * (v[i][j] + pb + gb)
                v[i][j] = min(v[i][j], vmax)
                v[i][j] = max(v[i][j], vmin)
            x[i] += v[i]
            y[i] = f(x[i])
            if y[i] < pbest_y[i]:
                pbest_x[i], pbest_y[i] = x[i], y[i]
            if y[i] < gbest_y:
                gbest_x, gbest_y = x[i], y[i]
    s1 = "Global Minimum: xmin = {0}, "
    s2 = "f(xmin) = {1:.6f}"
    ss = s1 + s2
    print(ss.format(gbest_x, gbest_y))
    return gbest_x, gbest_y


from datetime import datetime
s = datetime.now()
X, y = PSO()
e = datetime.now()
print("Running Time:", e - s)
print(Bounds(X) < 0) # 检查是否满足约束


'''
Global Minimum: xmin = [0.55216734 1.20325918 0.94782404], f(xmin) = 10.651092
Running Time: 0:00:01.557554
'''
