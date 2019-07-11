import numpy as np
from numpy.random import permutation, rand, randint
from numpy import exp, sqrt
import matplotlib.pyplot as plt

pos_x = [1, 3, 6, 12, 19, 22, 23, 20, 21, 22.5, 40, 44, 42, 36, 39, 58, 62, 88, 90, 83, 71, 67, 64, 52, 84, 87, 71, 71,
         58, 80, 1]
pos_y = [99, 50, 64, 40, 41, 42, 37, 54, 60, 60.5, 26, 20, 35, 83, 95, 33, 30.5, 6, 38, 44, 42, 57, 59, 62, 65, 74, 70,
         77, 68, 66, 99]

n = len(pos_x)
d = rand(n, n)
for i in range(n): # 计算距离
    for j in range(n):
        x1, y1 = pos_x[i], pos_y[i]
        x2, y2 = pos_x[j], pos_y[j]
        d[i][j] = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

y, path = 0x3f3f3f3f, None


def MonteCarlo():
    ''' 采用 Monte Carlo Algorithm 产生较好初始解 '''
    global y, path
    for _ in range(1000):
        path0 = permutation(n - 2)
        for i in range(n - 2):
            path0[i] += 1
        path0 = np.append(0, path0)
        path0 = np.append(path0, n - 1)
        tmp = 0
        for i in range(n - 1):
            tmp += d[path0[i], path0[i + 1]]
        if tmp < y:
            path, y = path0, tmp


def SA():
    global path, y, d, n
    T, finalT, coef = 1000, 1, 0.9  # 0.9 66 0.99 688
    K, niter = 1, 1000
    MonteCarlo()
    bestPath, bestY = None, 0x3f3f3f3f
    while T > finalT:
        for _ in range(niter):
            u, v = int(randint(1, n - 2, 1)), int(randint(1, n - 2, 1)) # 二变换产生新解
            if u > v: u, v = v, u
            if u == v: continue
            df = d[path[u - 1]][path[v]] + d[path[u]][path[v + 1]] - d[path[u - 1]][path[u]] - d[path[v]][path[v + 1]]
            if df < 0:
                while u < v:
                    path[u], path[v] = path[v], path[u]
                    u += 1
                    v -= 1
                y += df
            elif exp(-df / K * T) > rand():
                while u < v:
                    path[u], path[v] = path[v], path[u]
                    u += 1
                    v -= 1
                y += df
            if y < bestY:
                bestPath, bestY = path.copy(), y
        T *= coef
    return bestPath, bestY


if __name__ == '__main__':
    path_, time = SA()
    print("巡航顺序为", path_)
    print("巡航距离:", time)
    xx, yy = [], []
    for idx in path_:
        xx.append(pos_x[idx])
        yy.append(pos_y[idx])
    plt.plot(xx, yy, marker='>', mec='r', mfc='w', label="TSP-SA")
    plt.scatter(xx[0], yy[0], c='g', s=100)
    plt.show()

'''
巡航顺序为
 [ 0 14 13 23 28 26 27 25 24 29 22 21 20 19 18 17 16 15 11 10 12  6  5  4 3  1  7  9  8  2 30]
用时: 426.30580180786706
'''
