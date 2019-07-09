'''
 * SA: Simulated Annealing Algorithm
 * 最好多运行几次
 * Parameters:
 * nowT: 初始温度, finalT: 结束温度
 * niter: 迭代次数, coef: 衰减系数-attenuation coefficient
 * K: 衡量参数, step: 最大步长
 * 采用罚函数法将约束条件加入目标函数
'''
import numpy as np
from numpy import exp
from numpy.random import rand

def target_func(x:np.ndarray):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8

def Bounds(x:np.ndarray) -> np.ndarray:
    ''' constrains <= 0 '''
    ans = [-xx for xx in x]
    ans.append(-x[0] * x[0] + x[1] - x[2] * x[2])
    ans.append(x[0] + x[1] * x[1] + x[2] * x[2] - 20)
    ans.append(-x[0] - x[1] * x[1] + 2)
    ans.append(-x[0] - 2 * x[1] * x[1] + 3)
    return np.array(ans)

def f(x:np.ndarray):
    y, bnds = target_func(x), Bounds(x)
    penelty = 0x3f3f3f3f # 注意适当调整惩罚系数
    for value in bnds:
        if value > 0: # violation of constrains
            y += (penelty * value)
    return y


def SA() -> float:
    T, finalT, coef = 1000, 1, 0.96
    K, step, niter = 1, 1, 1000
    x, ansX = rand(3), rand(3)
    ansY = f(ansX)
    while T > finalT:
        for i in range(niter):
            y, ansY = f(x), f(ansX)
            newx = x + step * (2 * rand(3) - 1)
            newy = f(newx)
            df1, df2 = newy - y, newy - ansY
            if df1 < 0:
                x = newx
            elif exp(-df1 / (K * T)) > rand():
                x = newx
            if df2 < 0:
                ansX = newx
        T *= coef
    print("Best X =", ansX)
    print("min F(X) = %.4f" % (f(ansX)))
    return ansX


from datetime import datetime
s = datetime.now()
ans = SA()
print(target_func(ans))
e = datetime.now()
print("Running Time:", e - s)


'''
Best X = [1.01445542 1.01423368 0.13144296]
min F(X) = 10.0751
Running Time: 0:00:06.877635
'''
