import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 定义目标函数
def func(x, a, b, c):
    return a * np.exp(-b * x) + c

# 生成样本点，对函数值加上高斯噪声作为样本点
xdata = np.linspace(0, 4, 50)
# a=2.5, b=1.3, c=0.5
y = func(xdata, 2.5, 1.3, 0.5)
# np.random.seed(1027) # 设置随机种子
err_stdev = 0.2
# 生成均值为0，标准差为err_stdev=0.2的高斯噪声
noise = err_stdev * np.random.normal(size=xdata.size)
ydata = y + noise


plt.figure('拟合图')
plt.plot(xdata, ydata, 'b-', label='data')


'''利用curve_fit作简单的拟合，popt为拟合得到的参数,pcov是参数的协方差矩阵'''
popt, pcov = curve_fit(func, xdata, ydata)
plt.plot(xdata, func(xdata, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))


# 限定参数范围：0<=a<=3, 0<=b<=1, 0<=c<=0.5
popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))
plt.plot(xdata, func(xdata, *popt), 'g--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
