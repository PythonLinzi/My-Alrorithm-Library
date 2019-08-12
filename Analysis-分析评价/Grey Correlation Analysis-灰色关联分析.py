import numpy as np
from numpy import mean, min, max, ones, array, abs
from numpy import ndarray as arr


class GCA:
    ''' Grey Correlation Analysis-灰色关联分析法 '''
    def __init__(self, data:arr, direction=None):
        self.rho = 0.5 # resolution coefficient-分辨系数
        self.x, self.y = data[1:,:], data[0]
        self.n, self.m = data.shape
        self.dir = ones(shape=self.n - 1) # 指标正负向,默认正向
        if len(direction):
            self.dir = direction
        self.delta = ones(shape=(self.n - 1, self.m)).astype(np.float)
        self.w = array([1 / self.m for _ in range(self.m)]).astype(np.float) # 关联度权重
        self.r = array([0 for _ in range(self.n - 1)]).astype(np.float)


    def init_process(self):
        ''' 数据初始化处理 '''
        for i in range(self.n - 1):
            for j in range(1, self.m):
                if self.dir[i]:
                    self.x[i][j] /= self.x[i][0]
                else:
                    self.x[i][j] = self.x[i][0] / self.x[i][j]
        for j in range(1, self.m):
            self.y[j] /= self.y[0]
        for i in range(self.n - 1):
            self.x[i][0] = 1
        self.y[0] = 1
        return


    def analysis(self):
        self.init_process()
        x, y = self.x, self.y
        rho = self.rho
        for i in range(self.n - 1):
            for j in range(self.m):
                x[i][j] = abs(y[j] - x[i][j])
        m, M = min(x), max(x)
        for i in range(self.n - 1):
            for j in range(self.m):
                tmp = m + rho * M
                tmp /= (x[i][j] + rho * M)
                self.delta[i][j] = tmp
        for i in range(self.n - 1):
            self.r[i] = sum(self.w * self.delta[i])
        r = self.r
        R = [[r[i], i + 1] for i in range(len(r))]
        R.sort(key=lambda x: x[0], reverse=True)
        print(self.r)
        print(R)
        return r, R


# demo
data = [[13.6, 14.01, 14.54, 15.64, 15.69],
        [11.50, 13.0, 15.15, 15.3, 15.02],
        [13.76, 16.36, 16.90, 16.56, 17.3],
        [12.41, 12.70, 13.96, 14.04, 13.46],
        [2.48, 2.49, 2.56, 2.64, 2.59],
        [85, 85, 90, 100, 105],
        [55, 65, 75, 80, 80],
        [65, 70, 75, 85, 90],
        [12.80, 15.30, 16.24, 16.40, 17.05],
        [15.30, 18.40, 18.75, 17.95, 19.30],
        [12.71, 14.50, 14.66, 15.88, 15.70],
        [14.78, 15.54, 16.03, 16.87, 17.82],
        [7.64, 7.56, 7.76, 7.54, 7.70],
        [120, 125, 130, 140, 140],
        [80, 85, 90, 90, 95],
        [4.02, 4.25, 4.01, 4.06, 3.99],
        [13.1, 13.42, 12.85, 12.72, 12.56]]
data = array(data)
direction = ones(16)
direction[15] = direction[14] = 0
gca = GCA(data=data, direction=direction)
gca.analysis()

