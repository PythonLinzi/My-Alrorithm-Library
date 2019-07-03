import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return (x - 2) * (x + 3) * (x + 8) * (x - 9)


class SA():
    '''Simulated annealing algorithm'''
    def __init__(self, func, init_x, init_T, final_T, niter, attenuation_coef, low, high, k=1):
        self.func = func
        self.low = low # 最小取值
        self.high = high # 最大取值
        self.initT = init_T # 初始温度
        self.finalT = final_T # 最终温度
        self.iterT = niter # 迭代次数
        self.coef = attenuation_coef # 衰减系数 attenuation coefficient
        self.nowT = self.initT # 初始温度
        self.now_x = init_x # 初始估计值
        self.k = k # 衡量参数
        self.has_found = False

    def is_in_boundary(self, x):
        if x >= self.low and x <= self.high:
            return True
        return False

    def __is_better(self, df):
        return df < 0

    def search(self):
        while self.nowT > self.finalT:
            for i in range(1, self.iterT, 1):
                temp1 = self.func(self.now_x)
                new_x = self.now_x + (2 * np.random.rand() - 1)
                if self.is_in_boundary(new_x):
                    temp2 = self.func(new_x)
                    df = temp2 - temp1
                    if self.__is_better(df):
                        self.now_x = new_x
                    else:
                        p = np.exp(-df / (self.k * self.nowT))
                        if np.random.rand() < p:
                            self.now_x = new_x
            self.nowT = self.coef * self.nowT
        self.has_found = True

    def print_best_ans(self):
        if self.has_found:
            print('best x='+str(self.now_x)+', f(x)='+str(self.func(self.now_x)))
        else:
            print('haven\'t found answer!')
        return self.now_x


if __name__=='__main__':
    x = np.linspace(-10, 10, 1000)
    y = f(x)
    plt.plot(x, y)
    initx = 0
    plt.plot(initx, f(initx), 'or')

    sa = SA(f, 0, 1000, 1, 1000, 0.95, -10, 10)
    sa.search()
    best_ans = sa.print_best_ans()

    plt.plot(best_ans, f(best_ans), '*r')
    plt.annotate('best point', xy=(best_ans, f(best_ans)), xytext=(best_ans + 1, f(best_ans) + 999),
                 arrowprops=dict(facecolor='black', shrink=0.005))
    plt.savefig('sa.png')
    plt.show()
