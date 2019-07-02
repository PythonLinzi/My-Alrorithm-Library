import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

x = np.array([129, 140, 103.5, 88, 185.5, 195, 105, 157.5, 107.5, 77, 81, 162, 162, 117.5])
y = np.array([7.5, 141.5, 23, 147, 22.5, 137.5, 85.5, -6.5, -81, 3, 56.5, -66.5, 84, -33.5])
z = np.array([4, 8, 6, 8, 6, 8, 8, 9, 9, 8, 8, 9, 4, 9])
points = []
for i, xx in enumerate(x):
    points.append([xx, y[i]])

'''二维散乱节点插值'''
gridx, gridy = np.linspace(x.min(), x.max(), 100), np.linspace(y.min(), y.max(), 100)
#gridz1 = griddata(points, z, (gridx, gridy), method='cubic')
#gridz2 = griddata(points, z, (gridx, gridy), method='nearest')
gx, gy = np.meshgrid(gridx, gridy)
gridz1 = griddata(points, z, (gx, gy), method='cubic')
gridz2 = griddata(points, z, (gx, gy), method='nearest')

'''把cubic插值中不确定的值nan用neareest插值结果替换'''
n, m = gridz1.shape
for i in range(n):
    for j in range(m):
        if np.isnan(gridz1[i][j]):
            gridz1[i][j] = gridz2[i][j]


'''绘图'''
plt.subplot(121)
plt.imshow(gridz2.T, extent=(0, 1, 0, 1), origin='lower')
plt.subplot(122)
plt.imshow(gridz1.T, extent=(0, 1, 0, 1), origin='lower')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
surf = ax.plot_surface(gx, gy, gridz1, rstride=1, cstride=1, cmap='rainbow')
plt.colorbar(surf, shrink=0.5, aspect=5)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
