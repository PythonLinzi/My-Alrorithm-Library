import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

''' y'(t) = f(t, y) '''
''' demo: f''(t) + b * f'(t) + c * sin(f(t)) = 0 '''
# first step: transform
# f' = g,  g' = -b * g - c * sin(f)


def df(t, y):
    f, g = y
    dydt = [g, -0.25 * g - 5 * np.sin((f))]
    return dydt

y0 = [np.pi - 0.1, 0] # initial condition: f(0) = pi-0.1, g(0) = 0
t = np.linspace(0, 10, 101) # 待求解的点
ans = solve_ivp(fun=df, t_span=(0, 10), y0=y0, t_eval=t)
fy, gy = ans.y[0], ans.y[1]

plt.plot(t, fy, 'r', label='f(t)')
plt.plot(t, gy, 'b', label='g(t)')
plt.legend()
plt.show()
