import numpy as np
from numpy.random import permutation, rand, randint
from numpy import exp, sqrt
import matplotlib.pyplot as plt


class TSP:
    def __init__(self, pos_x, pos_y):
        self.pos_x, self.pos_y = pos_x, pos_y # XY坐标
        self.n, self.inf = len(pos_x), 0x3f3f3f3f
        self.d = rand(self.n, self.n)
        for i in range(self.n):
            for j in range(self.n):
                x1, y1 = pos_x[i], pos_y[i]
                x2, y2 = pos_x[j], pos_y[j]
                self.d[i][j] = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        self.y, self.path = 0x3f3f3f3f, None


    def __MonteCarlo(self):
        ''' use Monte Carlo Algorithm 产生较好初始解 '''
        y, path, n = self.y, self.path, self.n
        for _ in range(1000):
            path0 = permutation(n - 2)
            for i in range(n - 2):
                path0[i] += 1
            path0 = np.append(0, path0)
            path0 = np.append(path0, n - 1)
            path0 = np.append(path0, 0)
            tmp = 0
            for i in range(n):
                tmp += (self.d[path0[i]][path0[i + 1]])
            if tmp < y:
                path, y = path0, tmp
        self.path = path
        self.y = y


    def __SA(self):
        self.__MonteCarlo()
        path, y = self.path, self.y
        d, n = self.d, self.n
        T, finalT, coef = 1000, 1, 0.9 # 0.9 -> 66  0.99 -> 688
        K, niter = 1, 1000
        bp, by = None, 0x3f3f3f3f # Best Parh && Best Length
        while T > finalT:
            for _ in range(niter):
                u = int(randint(1, n - 2, 1))
                v = int(randint(1, n - 2, 1))
                if u > v:
                    u,v = v, u
                if u == v:
                    continue
                tmp1 = d[path[u - 1]][path[v]]
                tmp2 = d[path[u]][path[v + 1]]
                tmp3 = d[path[u - 1]][path[u]]
                tmp4 = d[path[v]][path[v + 1]]
                dy = tmp1 + tmp2 - tmp3 - tmp4
                if dy < 0:
                    while u < v:
                        path[u], path[v] = path[v], path[u]
                        u += 1
                        v -= 1
                    y += dy
                elif exp(-dy / K * T) > rand():
                    while u < v:
                        path[u], path[v] = path[v], path[u]
                        u += 1
                        v -= 1
                    y += dy
                if y < by:
                    bp, by = path.copy(), y
            T *= coef
        return bp, by


    def travel(self):
        bp, by = self.__SA()
        print("巡航顺序为", bp)
        print("巡航距离:", by)
        x, y =[], []
        for idx in bp:
            x.append(self.pos_x[idx])
            y.append(self.pos_y[idx])
        plt.plot(x, y, marker='>', mec='r', mfc='w', label="TSP-SA")
        plt.scatter(x[0], y[0], c='g', s=100)
        plt.grid()
        plt.show()
        return bp, by


if __name__ == '__main__':
    pos_x = [1, 3, 6, 12, 19, 22, 23, 20, 21, 22.5, 40, 44, 42, 36, 39, 58, 62, 88, 90, 83, 71, 67, 64, 52, 84, 87, 71,
             71, 58, 80, 1]
    pos_y = [99, 50, 64, 40, 41, 42, 37, 54, 60, 60.5, 26, 20, 35, 83, 95, 33, 30.5, 6, 38, 44, 42, 57, 59, 62, 65, 74,
             70, 77, 68, 66, 99]
    tsp = TSP(pos_x, pos_y)
    tsp.travel()


'''
巡航顺序为 [ 0  2  8  9  7  1  3  4  5  6 12 10 11 15 16 20 17 18 19 24 29 25 27 26
 21 22 28 23 13 14 30  0]
巡航距离: 433.2746386109633
'''

