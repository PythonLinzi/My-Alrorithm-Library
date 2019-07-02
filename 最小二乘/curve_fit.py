import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class CurveFit:
    def __init__(self, func, xdata:list, ydata:list):
        self.f = func
        self.x, self.y = xdata, ydata

    def fit(self):
        self.popt, self.pcov = curve_fit(
            self.f, xdata=self.x, ydata=self.y
        )
        return self.popt, self.pcov

    def fit_bnds(self, bnds):
        self.popt, self.pcov = curve_fit(
            self.f, xdata=self.x, ydata=self.y,
            bounds=bnds
        )
        return self.popt, self.pcov


    def evaluate(self):
        x, y = np.array(self.x), np.array(self.y)
        n = len(x)
        y_p = np.array(self.f(x, *self.popt))
        SSE = ((y - y_p) ** 2).sum() # 和方差、误差平方和
        MSE = SSE / n # 均方差、方差
        RMSE = np.sqrt(MSE) # 均方根、标准差
        SST = ((y - y.mean()) ** 2).sum()
        SSR = SST - SSE
        R_square = SSR / SST # 决定系数越接近1, 拟合效果越好, (R-square不适合用于判断非线性拟合的效果)
        # R_square_adjust = 1 - (1 - R_square ** 2) * (n - 1) / (n - p - 1) # p为特征个数
        return SSE, MSE, RMSE, R_square


    def show(self):
        plt.figure("拟合图像")
        plt.plot(self.x, self.y,
                 'b-', label="original data")
        x = np.linspace(min(self.x), max(self.x), 1000)
        plt.plot(x, self.f(x, *self.popt), 'r-', label="fit result")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()
        print("parameter:", tuple(self.popt))


if __name__ == '__main__':
    x = [19, 25, 31, 38, 44]
    y = [19, 32.3, 49, 73.3, 97.8]
    def f(x, a, b):
        return a + b * x ** 2
    curve = CurveFit(f, x, y)
    curve.fit() # 拟合参数a, b
    curve.show()
    print(curve.evaluate())
