'''
多运行几次
注意检查结果是否满足约束条件
'''

import numpy as np
from scipy.optimize import basinhopping as BH


def target_func(x:np.ndarray):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8


def f(x:np.ndarray):
    ''' constrains <= 0 '''
    ''' 采用罚函数法将约束条件加入目标函数 '''
    y = target_func(x)
    penelty = 0x3f3f3f3f # 惩罚系数(可以适当调整)
    bnds = -x[0] * x[0] + x[1] - x[2] * x[2]  # -x1^2 + x2 - x3^2 <= 0
    if bnds > 0: y += penelty * bnds # violation of constrains
    bnds = x[0] + x[1] * x[1] + x[2] * x[2] - 20  # x1 + x2^2 + x3^2 - 20 <= 0
    if bnds > 0: y += penelty * bnds
    bnds = -x[0] - x[1] * x[1] + 2  # -x1 - x2^2 + 2 <= 0
    if bnds > 0: y += penelty * bnds
    bnds = -x[1] - 2 * x[2] * x[2] + 3  # -x2 - 2 * x3^2 + 3 <= 0
    if bnds > 0: y += penelty * bnds
    return y


x0 = np.random.rand(3) # initial guess
mk = {"method": "L-BFGS-B"}
res = BH(func=f, x0=x0, niter=500, stepsize=0.5,
         minimizer_kwargs=mk)
print("Global Minimum: xmin = {0}, f(xmin) = {1:.6f}".format(res.x, res.fun))
