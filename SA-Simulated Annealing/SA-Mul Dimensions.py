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
    ans = [-xx for xx in x] # -X <= 0
    ans.append(-x[0] * x[0] + x[1] - x[2] * x[2]) # -x1^2 + x2 - x3^2 <= 0
    ans.append(x[0] + x[1] * x[1] + x[2] * x[2] - 20) # x1 + x2^2 + x3^2 - 20 <= 0
    ans.append(-x[0] - x[1] * x[1] + 2) # -x1 - x2^2 + 2 <= 0
    ans.append(-x[1] - 2 * x[2] * x[2] + 3) # -x2 - 2 * x3^2 + 3 <= 0
    return np.array(ans)

def f(x:np.ndarray):
    y, bnds = target_func(x), Bounds(x)
    penelty = 1e30 # 惩罚系数
    for value in bnds:
        if value > 0: # violation of constrains
            y += (penelty * value)
    return y


def SA() -> float:
    T, finalT, coef = 1000, 1, 0.9
    K, step, niter = 1, 1, 1000
    x, ansX = rand(3), rand(3) # 注意X要在X的取值范围内随机投点
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
    # 打印结果
    bnds, check = Bounds(ansX), True
    print(bnds) # 全部小于0则满足约束
    for bnd in bnds:
        if bnd > 0:
            check = False
    if check:
        print("满足约束条件!")
        print("Best X =", ansX)
        print("min F(X) = %f" % (f(ansX)))
    else:
        print("不满足约束条件!")
    return ansX


from datetime import datetime
s = datetime.now()
ans = SA()
print(target_func(ans))
e = datetime.now()
print("Running Time:", e - s)


'''
[-5.40383136e-01 -1.22208623e+00 -9.70183913e-01 -1.11845251e-02 -1.70248653e+01 -3.38778974e-02 -1.04599881e-01]
满足约束条件!
Best X = [0.54038314 1.22208623 0.97018391]
min F(X) = 10.726766
10.726765519164768
Running Time: 0:00:06.787844
'''
