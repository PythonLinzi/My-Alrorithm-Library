'''
 * SA: Simulated Annealing Algorithm
 * 最好多运行几次
 * Parameters:
 * nowT: 初始温度, finalT: 结束温度
 * niter: 迭代次数, coef: 衰减系数-attenuation coefficient
 * K: 衡量参数, step: 最大步长
'''
import numpy as np
from numpy import exp
from numpy.random import rand

def f(x:np.ndarray):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8

def in_bnds(x:np.ndarray):
    if not (x[0] > 0 and x[1] > 0 and x[2] > 0):
        return False
    if x[0] * x[0] - x[1] + x[2] * x[2] >= 0:
        if -x[0] - x[1] * x[1] - x[2] * x[2] + 20 >= 0:
            if x[0] + x[1] + x[1] - 2 >= 0:
                if x[1] + 2 * x[2] * x[2] - 3 >= 0:
                    return True
    return False


def SA() -> float:
    T, finalT, coef = 1000, 1, 0.96
    K, step, niter = 1, 1, 1000
    x, ans = rand(3), rand(3)
    while T > finalT:
        for i in range(niter):
            y = f(x)
            newx = x + step * (2 * rand(3) - 1)
            if in_bnds(newx):
                df = f(newx) - y
                if df < 0:
                    ans = x = newx
                elif exp(-df / (K * T)) > rand():
                    x = newx
        T *= coef
    print("Best X =", ans)
    print("min F(X) = %.4f" % (f(ans)))
    return ans


from datetime import datetime
s = datetime.now()
ans = SA()
e = datetime.now()
print("Running Time:", e - s)
print(f(np.array([0.3503, 0.8960, 0.8228])))

'''
Best X = [0.33218868 0.85070341 1.08381848]
min F(X) = 10.0087
Running Time: 0:00:02.275203
9.60252593
'''
