'''
 * SA: Simulated Annealing Algorithm
 * 最好多运行几次
 * Parameters:
 * nowT: 初始温度, finalT: 结束温度
 * niter: 迭代次数, coef: 衰减系数-attenuation coefficient
 * K: 衡量参数, step: 最大步长
'''
from numpy import exp
from numpy.random import rand

def f(x:float):
    return (x - 2) * (x + 3) * (x + 8) * (x - 9)

def in_bnds(x:float):
    return x > -10 and x < 10

def SA():
    ''' Simulated Annealing Algorithm '''
    T, finelT, coef = 1000, 1, 0.99
    K, step, niter = 1, 1, 1000
    x, ansX = rand(), 0
    while T > finelT:
        for i in range(niter):
            y = f(x)
            newx = x + step * (2 * rand() - 1)
            if in_bnds(newx):
                df = f(newx) - y
                if df < 0:
                    ansX = x = newx
                elif exp(-df / (K * T)) > rand():
                    x = newx
        T *= coef
    print('Best x = %.4f, min f(x) = %.4f' % (ansX, f(ansX)))
    return ansX

from datetime import datetime
s = datetime.now()
best_ans = SA()
e = datetime.now()
print(e - s)

# plot
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-10, 10, 1000)
y = f(x)
plt.plot(x, y, 'b', best_ans, f(best_ans), '*r')
plt.annotate('Best Point', xy=(best_ans, f(best_ans)), xytext=(best_ans + 1, f(best_ans) + 999),
                 arrowprops=dict(facecolor='black', shrink=0.005))
plt.show()
