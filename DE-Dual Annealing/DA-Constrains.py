import numpy as np
from scipy.optimize import dual_annealing as DA

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

bnds = [(0, 100), (0, 100), (0, 100)]
res = DA(func=f, bounds=bnds, maxiter=1000, seed=1234)
print("global minimum: xmin = {0}, f(xmin) = {1:.6f}".format(res.x, res.fun))
