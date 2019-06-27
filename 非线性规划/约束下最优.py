from scipy.optimize import minimize

f = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2
init_guess = (2, 0)
cons = (
    {'type': 'ineq', 'fun': lambda x: x[0] - 2 * x[1] + 2},
    {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},
    {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2}
)
bnds = ((0, None), (0, None))
res = minimize(f, init_guess, method='SLSQP', bounds=bnds, constraints=cons)
print(res)



'''-----------------------------------------------------'''
from scipy.optimize import minimize

f = lambda x: x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + 8
init_guess = (0.5, 1, 1)
cons = (
    {'type': 'ineq', 'fun': lambda x: x[0] ** 2 - x[1] + x[2] ** 2},
    {'type': 'ineq', 'fun': lambda x: -x[0] - x[1] ** 2 - x[2] ** 2 + 20},
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] ** 2 - 2},
    {'type': 'eq', 'fun': lambda x: x[1] + 2 * x[2] ** 2 - 3}
)
bnds = ((0, None), (0, None), (0, None))
res = minimize(f, init_guess, method='SLSQP', bounds=bnds, constraints=cons)
print(res)


'''
init_guess 初始值估计
cons = (
    # 约束条件 分为eq 和ineq
    #eq表示 函数结果等于0 ； ineq 表示 表达式大于等于0
    {'type': 'ineq', 'fun': lambda x: x[0] ** 2 - x[1] + x[2] ** 2},
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] ** 2 - 2},
)
bnds 取值范围
'''
