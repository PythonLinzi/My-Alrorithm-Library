import numpy as np
from scipy.optimize import basinhopping


''' 选取不同初始值多运行几次(run from a number of different starting points) '''
''' take two-D as example '''
# demo1: compute directly, without gradient
def func(x):
    return np.cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] + 0.2) * x[0]

x0 = np.array([1.0, 1.0]) # initial guess
minimizer_kwargs = {"method": "L-BFGS-B"}
ans = basinhopping(func=func, x0=x0, niter=300, stepsize=0.5,
                   minimizer_kwargs=minimizer_kwargs)
print("Global minimum: x = [%.4f, %.4f], f(%.4f, %.4f) = %.4f" % (ans.x[0], ans.x[1], ans.x[0], ans.x[1], ans.fun))


'''----------------------------------------------------分割线--------------------------------------------------------'''
# demo2 : use gradient information to speed up computation -- jac: True
def func(x):
    f = np.cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] + 0.2) * x[0]
    df = np.zeros(2)
    df[0] = -14.5 * np.sin(14.5 * x[0] - 0.3) + 2. * x[0] + 0.2 # x1的偏导
    df[1] = 2. * x[1] + 0.2 # x2的偏导
    return f, df

x0 = np.array([1.0, 1.0]) # initial guess
minimizer_kwargs = {"method": "L-BFGS-B", "jac": True}
ans = basinhopping(func=func, x0=x0, niter=300, stepsize=0.5,
                   minimizer_kwargs=minimizer_kwargs)
print("Global minimum: x = [%.4f, %.4f], f(%.4f, %.4f) = %.4f" % (ans.x[0], ans.x[1], ans.x[0], ans.x[1], ans.fun))


'''----------------------------------------------------分割线--------------------------------------------------------'''
# demo3: set take_step and bounds for differenr varible
# and use callback to record (x, local_min_y) in every step
class TakeStep(object):
    def __init__(self, stepsize=0.5):
        self.stepsize = stepsize
    def __call__(self, x: np.ndarray):
        s = self.stepsize
        x[0] += np.random.uniform(-2 * s, 2 * s)
        x[1:] += np.random.uniform(-s, s, x[1:].shape)
        return x

class Bounds(object):
    def __init__(self, xmax=[1.1,1.1], xmin=[-1.1,-1.1]):
        self.xmax, self.xmin = np.array(xmax), np.array(xmin)
    def __call__(self, **kwargs):
        x = l=kwargs["x_new"]
        tmax, tmin = bool(np.all(x <= self.xmax)), bool(np.all(x >= self.xmin))
        return tmax and tmin


xdata, ydata = [], []
def save(x, f, accepted): # use for callback
    xdata.append(x)
    ydata.append(f)


def func(x):
    f = np.cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] + 0.2) * x[0]
    df = np.zeros(2)
    df[0] = -14.5 * np.sin(14.5 * x[0] - 0.3) + 2. * x[0] + 0.2 # x1的偏导
    df[1] = 2. * x[1] + 0.2 # x2的偏导
    return f, df

takstep, bnds = TakeStep(), Bounds()
x0 = np.array([1.0, 1.0]) # initial guess
minimizer_kwargs = {"method": "L-BFGS-B", "jac": True}
ans = basinhopping(func=func, x0=x0, niter=300, minimizer_kwargs=minimizer_kwargs,
                   take_step=takstep, accept_test=bnds, callback=save)
# callback: call function "save" to record (x, miny) in every step

xdata, ydata = np.array(xdata), np.array(ydata)
xmin, ymin = xdata[ydata.argmin()], ydata.min()
print("Global minimum: x = [%.4f, %.4f], f(%.4f, %.4f) = %.4f" % (ans.x[0], ans.x[1], ans.x[0], ans.x[1], ans.fun))
print("Global minimum: x = [%.4f, %.4f], f(%.4f, %.4f) = %.4f" % (xmin[0], xmin[1], xmin[0], xmin[1], ymin)) #comprare
