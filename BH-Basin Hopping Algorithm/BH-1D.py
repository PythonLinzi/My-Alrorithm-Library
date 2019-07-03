import numpy as np
from scipy.optimize import basinhopping


''' 选取不同初始值多运行几次(run from a number of different starting points) '''
''' one-dimensionnal '''
# demo1: compute directly, without gradient
func = lambda x: np.cos(14.5 * x - 0.3) + (x + 0.2) * x
x0 = np.array([1]) # initial guess
minimizer_kwargs = {"method": "BFGS"}
ans = basinhopping(func=func, x0=x0, niter=100, T=1.0,
                   stepsize=0.5, minimizer_kwargs=minimizer_kwargs)
print("global minimum: x = %.4f, f(%.4f) = %.4f" % (ans.x, ans.x, ans.fun))


'''----------------------------------------------------分割线--------------------------------------------------------'''
# demo2 : use gradient information to speed up computation -- jac: True
xdata, ydata = [], []
def save(x, f, accepted):
    xdata.append(x[0])
    ydata.append(f)

def func(x):
    f = np.cos(14.5 * x - 0.3) + (x + 0.2) * x
    df = -14.5 * np.sin(14.5 * x - 0.3) + 2 * x + 0.2
    return f, df
x0 = np.array([1]) # initial guess
minimizer_kwargs = {"method": "BFGS", "jac": True}
res = basinhopping(func=func, x0=x0, niter=200, T=1.0,
                   stepsize=0.5, minimizer_kwargs=minimizer_kwargs,
                   callback=save) # call function "save" to record (x, miny) in every step
xdata, ydata = np.array(xdata), np.array(ydata)
xmin, ymin = xdata[ydata.argmin()], ydata.min()
print("global minimum: x = %.4f, f(%.4f) = %.4f" % (xmin, xmin, ymin))

# bounds setting refer to BH-Multiple Demension.py---demo3
