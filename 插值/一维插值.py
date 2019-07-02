from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np


x = [0, 3, 5, 7, 9, 11, 12, 13, 14, 15]
y = [0, 1.2, 1.7, 2, 2.1, 2, 1.8, 1.2, 1, 1.6]
'''分段线性 piecewise linear'''
f1 = interp1d(x, y)
print(f1)
'''立方插值 cubic interpolation'''
f2 = interp1d(x, y, kind='cubic')
print(f2)

xnew = np.linspace(0, 15, 1000)
plt.plot(x, y, 'o', xnew, f1(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'])
plt.show()
