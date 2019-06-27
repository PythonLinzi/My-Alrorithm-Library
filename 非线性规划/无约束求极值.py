from scipy.optimize import minimize_scalar, minimize

'''一元函数'''
f = lambda x: (x - 2) * x * (x + 2) ** 2
res = minimize_scalar(f)
print(res)
ans = minimize_scalar(f, bounds=(-3, -1), method='bounded')
print(ans)


'''多元函数'''
f = lambda x: x[0] ** 3 - x[1] ** 3+ 3 * x[0] ** 2+ 3 * x[1] ** 2- 9 * x[0]
bnds = ((-10, 10), (-10, 10))
x0 = (1, 1) #初始解估计
res = minimize(f, x0, method='SLSQP')
print(res)
