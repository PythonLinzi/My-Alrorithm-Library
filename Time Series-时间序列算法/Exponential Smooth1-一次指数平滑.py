import numpy as np


def smooth1(ydata:np.ndarray, alpha=0.2, k=2):
    ''' 一次指数平滑法 -- 一般只预测一期'''
    S = [sum(ydata[:k]) / k] # initial value
    for y in ydata:
        s = int((alpha * y + (1 - alpha) * S[-1]) * 100) / 100 # 控制两位小数
        # s = alpha * y + (1 - alpha) * S[-1]
        S.append(s)
    n = len(ydata)
    err = np.sqrt(sum((ydata - S[:n]) ** 2) / n) # 标准误差
    return S, err


# demo
t = np.linspace(1, 12, 12)
ydata = np.array([50, 52, 47, 51, 49, 48, 51, 40, 48, 52, 51, 59])
newy, err = smooth1(ydata=ydata)
print(newy)
print("标准误差为 %.2f" % (err))
print("下一期预测值为 %.2f" % (newy[-1]))
