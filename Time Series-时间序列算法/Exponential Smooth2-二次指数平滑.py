import numpy as np
import matplotlib.pyplot as plt


def smooth2(ydata:np.ndarray, alpha=0.2, k=1):
    ''' 二次指数平滑法 '''
    S1, S2 = [sum(ydata[:k]) / k], [sum(ydata[:k]) / k]  # initial value
    for y in ydata:
        tmp = S1[-1]
        S1.append(alpha * y + (1 - alpha) * tmp)
        tmp = S2[-1]
        S2.append(alpha * S1[-1] + (1 - alpha) * tmp)
    a, b, y,  n = [], [], [], len(S1)
    for i in range(n):
        a.append(2 * S1[i] - S2[i])
        b.append(alpha * (S1[i] - S2[i]) / (1 - alpha))
        y.append(a[-1] + b[-1])
    y ,a, b = np.array(y), np.array(a), np.array(b)
    err = np.sqrt(sum((ydata[:] - y[:n - 1]) ** 2) / (n - 1))
    return y ,a, b, err


def forecast(data:np.ndarray, alpha=0.2, k=1, num=5):
    ''' 预测接下来的 num 期 '''
    y, a, b, err = smooth2(ydata=data, alpha=alpha, k=k)
    print(len(data), len(y))
    print("标准误差为 %.2f" % (err))
    a, b = a[-1], b[-1]
    for i in range(2, num + 1):
        nxt_y = a + b * i
        y = np.append(y, nxt_y)
    return y


demo_data = [676, 825, 774, 716, 940, 1159, 1384, 1524, 1668, 1688, 1958,
             2031, 2234, 2566, 2820, 3006, 3093, 3277, 3514, 3770, 4107]
demo_data = np.array(demo_data)
t = np.linspace(1, 21, 21)
plt.plot(t, demo_data, 'b', label="original")
num = 5
t = np.linspace(1, 21 + num, 21 + num)

e, best_alpha = 1000, 0
alpha_span = np.linspace(0, 0.89, 90)
for al in alpha_span:
    y, a, b, err = smooth2(ydata=demo_data, alpha=al, k=3)
    if err < e:
        best_alpha = al
print("Alpha = %.2f" % (best_alpha))
y_forecast = forecast(data=demo_data, alpha=best_alpha, k=2, num=num)
plt.plot(t, y_forecast, 'r', label="forecast")
plt.legend()
plt.show()
