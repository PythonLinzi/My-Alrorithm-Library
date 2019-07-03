import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


''' demo: f''(t) + b * f'(t) + c * sin(f(t)) = 0 '''
# first step: transform
# f'(t) = g(t)
# g'(t) = -b * g(t) - c * sin(f(t))

def pend(y, t, b, c):
    f, g = y
    dydt = [g, -b * g - c * np.sin((f))]
    return dydt

b, c = 0.25, 5.0
y0 = [np.pi - 0.1, 0] # initial condition: f(0) = pi-0.1, g(0) = 0
t = np.linspace(0, 10, 101) # 待求解的点
sol = odeint(func=pend, y0=y0,t=t, args=(b, c))

plt.plot(t, sol[:, 0], 'r', label='f(t)')
plt.plot(t, sol[:, 1], 'b', label='g(t)')
plt.legend(loc='best')
plt.show()

'''
scipy.integrate.odeint(func, y0, t, args=(), Dfun=None, col_deriv=0, full_output=0, ml=None,
                      mu=None, rtol=None, atol=None, tcrit=None, h0=0.0, hmax=0.0,
                      hmin=0.0, ixpr=0, mxstep=0, mxhnil=0, mxordn=12, mxords=5, printmessg=0)
前四个参数较为重要
Parameters:
           func : callable(y, t0, ...)------Computes the derivative of y at t0.
           y0 : array------Initial condition on y (can be a vector).
           t : array------A sequence of time points for which to solve for y.
                          The initial value point should be the first element of this sequence.
           args : tuple, optional------Extra arguments to pass to function
Returns:
        y : array, shape (len(t), len(y0))------Array containing the value of y for each desired time in t, 
                                                with the initial value y0 in the first row.
        infodict : dict, only returned if full_output == True Dictionary containing additional output information
'''
