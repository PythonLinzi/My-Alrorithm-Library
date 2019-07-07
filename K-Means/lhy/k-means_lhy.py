from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np


class K_Means:
    def __init__(self, data, k=2, iter_times=1000):
        self.k = k
        self.iter_times = iter_times
        self.n = len(data)
        self.data = data
        self.ck = []
        i = 0
        while i < self.k:
            a = np.random.randint(0, self.n)
            if data[a] not in self.ck:
                self.ck.append(data[a])
                i += 1



    def Minkowski(self, x1, y1, x2, y2, p=2):
        dis = (x1 - x2) ** p + (y1 - y2) ** p
        return dis ** (1 / p)


    def choose(self, x):
        dis = self.Minkowski(x[0], x[1], self.ck[0][0], self.ck[0][1])
        ans = 0
        for i in range(1, self.k):
            tmp = self.Minkowski(x[0], x[1], self.ck[i][0], self.ck[i][1])
            if tmp < dis:
                dis = tmp
                ans = i
        return ans


    def kmeans(self):
        category = None
        for _ in range(self.iter_times):
            C = [[] for i in range(self.k)]
            for x in self.data:
                idx = self.choose(x)
                C[idx].append(x)
            l = len(self.ck[0])
            category = C.copy()
            for i in range(self.k):
                isize = len(C[i])
                for j in range(l):
                    tmp = 0
                    for x in C[i]:
                        tmp += x[j]
                    tmpci = tmp / isize
                    if tmpci != self.ck[i][j]:
                        self.ck[i][j] = tmpci
        return category


    def main(self):
        category = self.kmeans()
        print(len(category[0]), category[0])
        print(len(category[1]), category[1])
        print(len(category[2]), category[2])
        color = ['r', 'g', 'b', 'w']
        for i in range(self.k):
            tmp = np.array(category[i])
            plt.scatter(tmp[:, 0], tmp[:, 1], c=color[i])
        plt.show()


if __name__ == '__main__':
    data = [[0.697, 0.460], [0.774, 0.376], [0.634, 0.264], [0.608, 0.318], [0.556, 0.215], [0.403, 0.237],
            [0.481, 0.149], [0.437, 0.211], [0.666, 0.091], [0.243, 0.267], [0.245, 0.057], [0.343, 0.099],
            [0.639, 0.141], [0.657, 0.198], [0.360, 0.370], [0.593, 0.042], [0.719, 0.103], [0.359, 0.188],
            [0.339, 0.241], [0.282, 0.257], [0.748, 0.232], [0.714, 0.346], [0.483, 0.312], [0.478, 0.437],
            [0.525, 0.369], [0.751, 0.489], [0.532, 0.472], [0.473, 0.376], [0.725, 0.455], [0.446, 0.459]]
    data_ = [[1, 1], [1, 1.1], [1, 0.9], [0.9, 0.99],
            [100, 1], [100, 1.1], [100, 0.9], [90, 0.99],
            [25, 1], [24, 1.1], [20, 0.9], [20.9, 0.99]]
    x, y = make_blobs(150)
    xxx = [list(xx) for xx in x]
    #print(xxx)
    km = K_Means(xxx, k=3)
    km.main()
