import numpy as np
from numpy import exp, sin, pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n, m = 51, 2001
x, t = np.linspace(0, 1, n), np.linspace(0, 2, m)
u = np.zeros(shape=(n, m))
dx, dt = x[1] - x[0], t[1] - t[0]
for i in range(n): u[i][0] = sin(pi * x[i])
for j in range(m): u[0][j] = 0


for j in range(0, m - 1):
    for i in range(1, n):
        if i == n - 1:
            u[i][j + 1] = u[i - 1][j + 1] - pi * exp(-(t[j + 1])) * dx
        else:
            u[i][j + 1] = u[i][j] + dt * (u[i + 1][j] - 2 * u[i][j] + u[i - 1][j]) / ((pi * dx) ** 2)
            u[i][j + 1] = u[i][j] + dt * (u[i + 1][j] - 2 * u[i][j] + u[i - 1][j]) / ((pi * dx) ** 2)


def plot3d(x,y,z):
    ''' surface plot '''
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='rainbow')
    ax.set_zlim(0, 1.2)
    ax.set_xlabel('pos: x')
    ax.set_ylabel('time: t')
    ax.set_zlabel('res: z')
    ax.set_title('PDE-demo1')
    plt.show()

x, t = np.meshgrid(x, t)
u = np.transpose(np.array(u))
print(x.shape, t.shape, u.shape)
plot3d(x, t, u)

r = dt / ((pi * dx) ** 2)
print("r = %f" % (r))
