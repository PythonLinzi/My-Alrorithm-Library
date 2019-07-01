import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp2d

x = np.linspace(100, 500, 5)
y = np.linspace(100, 400, 4)
x, y =np.meshgrid(x, y)

z = [[636, 697, 624, 478, 450], [698, 712, 630, 478, 420],
     [680, 674, 598, 412, 400], [662, 626, 552, 334, 310]]
z = np.array(z)

'''二维插值'''
f = interp2d(x, y, z, kind='cubic')
#"nearest","zero"为阶梯插值
#slinear 线性插值
#"quadratic","cubic" 为2阶、3阶B样条曲线插值

'''plot-original'''
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
surf1 = ax1.plot_surface(x, y, z, rstride=1, cstride=1, cmap='rainbow')
plt.colorbar(surf1, shrink=0.5, aspect=5) #标注

'''plot-interpolation'''
xnew = np.linspace(100, 500, 100)
ynew = np.linspace(100, 400, 100)
znew = f(xnew, ynew)
xnew, ynew = np.meshgrid(xnew, ynew)

fig2 = plt.figure()
ax2 = fig2.add_subplot(1, 1, 1, projection='3d')
surf2 = ax2.plot_surface(xnew, ynew, znew, rstride=1, cstride=1, cmap='rainbow')
plt.colorbar(surf2, shrink=0.5, aspect=5)
plt.show()
