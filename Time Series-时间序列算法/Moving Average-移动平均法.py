import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(1, 11, 11)
y = [533.8, 574.6, 606.9, 649.8, 705.1, 772,
     816.4, 892.7, 963.9, 1015.1, 1102.7]

def moving_average(y: list, N: int):
    ''' 一次移动平均法 '''
    T, y_p = len(y), [sum(y[:N]) / N]
    for t in range(N, T):
        M = y_p[-1] + (y[t] - y[t - N]) / N
        y_p.append(M)
    y, y_p = np.array(y), np.array(y_p)
    err = np.sqrt(sum((y[N:] - y_p[:len(y_p) - 1]) ** 2) / (T - N))
    print("预测值为 %.2f, 标准误差为 %.2f" % (y_p[-1], err))
    return y_p, err


yp, e = moving_average(y, 4)
newy = np.append(np.array(y)[:4], yp)
newt = np.linspace(1, 12, 12)
moving_average(y, 5)
plt.plot(t, y, 'b', label="original")
plt.plot(newt, newy, 'r', label="Predict")
plt.show()
