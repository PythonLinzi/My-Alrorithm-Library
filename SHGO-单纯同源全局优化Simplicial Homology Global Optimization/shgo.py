from scipy.optimize import shgo

f = lambda x: x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + 8
# constrains >= 0
cons = (
    {'type': 'ineq', 'fun': lambda x: x[0] ** 2 - x[1] + x[2] ** 2},
    {'type': 'ineq', 'fun': lambda x: -x[0] - x[1] ** 2 - x[2] ** 2 + 20},
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] ** 2 - 2},
    {'type': 'eq', 'fun': lambda x: x[1] + 2 * x[2] ** 2 - 3}
)
bnds = ((0, None), (0, None), (0, None))

ans = shgo(func=f, bounds=bnds, constraints=cons)

print(ans.x, ans.fun)
