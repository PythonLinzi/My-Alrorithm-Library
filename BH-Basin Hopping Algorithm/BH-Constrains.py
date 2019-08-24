'''
To improve your chances of finding a global minimum:
 *use higher popsize values,
 *with higher mutation and (dithering),
 *but lower recombination values.
 This has the effect of widening the search radius, but slowing convergence.
'''
import numpy as np
from scipy.optimize import differential_evolution as DE


def target_func(x:np.ndarray):
    return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8


def f(x:np.ndarray):
    ''' constrains <= 0 '''
    ''' 采用罚函数法将约束条件加入目标函数 '''
    y = target_func(x)
    penelty = 1e30 # 惩罚系数
    bnds = -x[0] * x[0] + x[1] - x[2] * x[2]  # -x1^2 + x2 - x3^2 <= 0
    if bnds > 0: y += penelty * bnds # violation of constrains
    bnds = x[0] + x[1] * x[1] + x[2] * x[2] - 20  # x1 + x2^2 + x3^2 - 20 <= 0
    if bnds > 0: y += penelty * bnds
    bnds = -x[0] - x[1] * x[1] + 2  # -x1 - x2^2 + 2 <= 0
    if bnds > 0: y += penelty * bnds
    bnds = -x[1] - 2 * x[2] * x[2] + 3  # -x2 - 2 * x3^2 + 3 <= 0
    if bnds > 0: y += penelty * bnds
    return y

bnds = [(0, 100), (0, 100), (0, 100)]
res = DE(func=f, bounds=bnds, maxiter=1000, popsize=25,
         mutation=(0.5, 1), recombination=0.7, tol=0.01)
print("Global Minimum: xmin = {0}, f(xmin) = {1:.6f}".format(res.x, res.fun))
