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


def target_func(x):
    return (x - 2) * (x + 3) * (x + 8) * (x - 9)


def Bounds(x):
    ''' constrains <= 0  '''
    bnds = [x - 10, -x - 10]
    return np.array(bnds)


def f(x):
    y, bnds = target_func(x), Bounds(x)
    penelty = 0x3f3f3f3f # 注意适当调整惩罚系数
    for value in bnds:
        if value > 0: # violation of constrains
            y += (penelty * value)
    return y


def SA():
    ''' Simulated Annealing Algorithm '''
    T, finelT, coef = 1000, 1, 0.96
    K, step, niter = 1, 1, 1000
    x, ansX = rand(1), rand(1)
    y, ansY = f(x), f(ansX)
    while T > finelT:
        for i in range(niter):
            y, ansY = f(x), f(ansX)
            newx = x + step * (2 * rand(1) - 1)
            newy = f(newx)
            df1, df2 = newy - y, newy - ansY
            if df1 < 0:
                x = newx
            elif exp(-df1 / (K * T)) > rand(1):
                x = newx
            if df2 < 0:
                ansX = newx
        T *= coef
    print('Best x = %.4f, min f(x) = %.4f' % (ansX, f(ansX)))
    return ansX


from datetime import datetime
s = datetime.now()
best_ans = SA()
e = datetime.now()
print(e - s)


# plot
import matplotlib.pyplot as plt
x = np.linspace(-10, 10, 1000)
y = target_func(x)
plt.plot(x, y, 'b', best_ans, f(best_ans), '*r')
plt.annotate('Best Point', xy=(best_ans, f(best_ans)), xytext=(best_ans + 1, f(best_ans) + 999),
                 arrowprops=dict(facecolor='black', shrink=0.005))
plt.show()
