import numpy as np
from scipy.optimize import least_squares

# demo1: min f1**2 + f2**2 + f3**2 + f4**2
def f(x):
    return np.array([
        0.0372 * x[0] + 0.2869 * x[1] - 0.8587, # f1
        0.6861 * x[0] + 0.7071 * x[1] - 0.1781, # f2
        0.6233 * x[0] + 0.6245 * x[1] - 0.0747, # f3
        0.6344 * x[0] + 0.6170 * x[1] - 0.8405  # f4
    ])


x0 = np.array([0.1, 0.5])
ans= least_squares(f, x0=x0, bounds=(0, 10))
print(ans)
print("best x =", ans.x)
'''
问题为求解非负的 X = [x1, x2]',  s.t. min ||CX - D|| ** 2
C = [[0.0372, 0.2869], [0.6861, 0.7071], [0.6233, 0.6245], [0.6344, 0.6170]]
D = [[0.8587], [0.1781], [0.0747], [0.8405]]
'''

print("---------分割线-----------")
# demo2: min 100 * (y - x**2)**2 + (1 - x)**2
def fun_rosenbrock(x):
    return np.array([10 * (x[1] - x[0]**2), (1 - x[0])])

x0_ = np.array([2, 2])
res = least_squares(fun_rosenbrock, x0=x0_)

print(res.x)
print(res.cost)
print(res.optimality)
