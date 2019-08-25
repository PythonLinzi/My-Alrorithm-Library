'''
 * SA: Simulated Annealing Algorithm
 * 最好多运行几次
 * Parameters:
 * nowT: 初始温度
 * finalT: 结束温度
 * niter: 迭代次数
 * coef: 衰减系数-attenuation coefficient
 * K: 衡量参数, step: 最大步长
 * 采用罚函数法将约束条件加入目标函数
'''
import numpy as np
from numpy import exp, array
from numpy.random import rand
from numpy import ndarray


class SA:
    ''' Simulated Annealing '''
    def __init__(self, f, niter=100, T=1e3, fT=1, ac=0.9, D=1):
        '''
        Params Initialize
        :param f: Target Funcion(Min)
        :param niter: int, number of iterations
        :param T: float, initial temperature
        :param fT: float, final temperature
        :param ac: float, attenuation coefficient
        :param D: int, dimensions of vars
        '''
        self.f = f
        self.niter = niter
        self.T = T
        self.fT = fT
        self.ac = ac
        self.D = D
        self.x0 = rand(D)
        self.K = 1
        self.step = 1

    def set_x0(self, x0):
        '''
        Set init x
        :param x0: init guess
        :return: None
        '''
        self.x0 = x0

    def set_K(self, k):
        '''
        Coeff K's setting
        :param k: coef
        :return: None
        '''
        self.K = k

    def set_step(self, step):
        '''
        Step Setting
        :param step: step
        :return: None
        '''
        self.step = step

    def compute(self):
        f = self.f
        niter = self.niter
        T, ft = self.T, self.fT
        ac = self.ac
        D = self.D
        x = self.x0
        y = f(x)
        ret_X = self.x0
        ret_Y = self.f(x)
        K = self.K
        step = self.step
        sche = "niter = {0}, y = {1}"
        cnt = 0
        while T > ft:
            for i in range(niter):
                cnt += 1
                print(sche.format(cnt, ret_Y))
                y, ret_Y = f(x), f(ret_X)
                new_X = x + step * (2 * rand(D) - 1)
                new_Y = f(new_X)
                dy1 = new_Y - y
                dy2 = new_Y - ret_Y
                if dy1 < 0:
                    x = new_X
                    y = new_Y
                elif exp(-dy1 / (K * T)) > rand():
                    x = new_X
                    y = new_Y
                if dy2 < 0:
                    ret_X = new_X
                    ret_Y = new_Y
            T *= ac
        s1 = "Global Minimum: xmin = {0}, "
        s2 = "f(xmin) = {1:.6f}"
        ss = s1 + s2
        print(ss.format(ret_X, ret_Y))
        return ret_X, ret_Y


if __name__ == '__main__':
    def target_func(x: ndarray):
        return x[0] * x[0] + x[1] * x[1] + x[2] * x[2] + 8


    def Bounds(x: np.ndarray) -> ndarray:
        ''' constrains <= 0 '''
        ans = [-xx for xx in x]  # -X <= 0
        ans.append(-x[0] * x[0] + x[1] - x[2] * x[2])  # -x1^2 + x2 - x3^2 <= 0
        ans.append(x[0] + x[1] * x[1] + x[2] * x[2] - 20)  # x1 + x2^2 + x3^2 - 20 <= 0
        ans.append(-x[0] - x[1] * x[1] + 2)  # -x1 - x2^2 + 2 <= 0
        ans.append(-x[1] - 2 * x[2] * x[2] + 3)  # -x2 - 2 * x3^2 + 3 <= 0
        return np.array(ans)


    def f(x: ndarray):
        y, bnds = target_func(x), Bounds(x)
        penelty = 1e30  # 惩罚系数
        for value in bnds:
            if value > 0:  # violation of constrains
                y += (penelty * value)
        return y

    sa = SA(f=f, niter=1000, T=1e3, fT=1, ac=0.9, D=3)
    x, y = sa.compute()
    if np.all(Bounds(x) <= 0):
        print("满足约束!")

