from scipy.optimize import lsq_linear

''' Solve a linear least-squares problem with bounds on the variables '''
''' min 0.5 * ||A x - b||**2  subject to lb <= x <= ub '''
A = [[0.0372, 0.2869], [0.6861, 0.7071], [0.6233, 0.6245], [0.6344, 0.6170]]
B = [0.8587, 0.1781, 0.0747, 0.8405]

res = lsq_linear(A=A, b=B, bounds=(0, 10))
print(res)
