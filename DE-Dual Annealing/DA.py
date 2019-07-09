import numpy as np
from scipy.optimize import dual_annealing as DA

func = lambda x: np.sum(x * x - 10 * np.cos(2 * np.pi * x)) + 10 * np.size(x)
lw = [-5.12] * 10
up = [5.12] * 10
res = DA(func=func, bounds=list(zip(lw, up)), maxiter=1000, seed=1234)
print("global minimum: xmin = {0}, f(xmin) = {1:.6f}".format(res.x, res.fun))
