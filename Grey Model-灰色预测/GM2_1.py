import numpy as np
from numpy import exp, array, zeros, abs
from numpy.random import rand
from scipy.optimize import least_squares
from scipy.optimize import dual_annealing as DA
from scipy.optimize import differential_evolution as DE


class GM_11:
    def __init__(self, data, nxt=3):
        self.x0 = array(data)
        self.n = len(data)
        self.x1 = array(data)
        self.ax1 = self.x1.copy()
        self.shape = self.x0.shape
        self.z = zeros(shape=self.shape)
        self.m = self.n + nxt # 预测后nxt期
        self.x1_p = zeros(shape=self.m)
        self.x1_p[0] = data[0]
        self.x0_p = self.x1_p.copy()
        self.a, self.b = 0, 0
        self.bnds = [exp(-2 / (self.n + 1)), exp(2 / (self.n + 1))]


    def __process_data(self):
        tmp = 0
        for i, x in enumerate(self.x0):
            tmp += x
            self.x1[i] = tmp
            if i > 0:
                self.z[i] = 0.5 * tmp + 0.5 * self.x1[i - 1]
                self.ax1[i] = self.x0[i] - self.x0[i - 1]


    def __f_lsq(self, AB) -> np.ndarray:
        ''' 最小二乘目标 '''
        res = []
        for i in range(1, self.n):
            tmp = self.ax1[i] + AB[0] * self.x0[i] + AB[1] * self.z[i] - AB[2]
            res.append(tmp)
        return array(res)


    def __lsq(self, bnds=(-100, 100)):
        """ Least Squares
        Parameters:
            bnds: tuple-like, the bounds of result
            a0: initial value guessed
        Returns:
            ans.x: fitted coefficients
        """
        a0 = ([rand(), rand(), rand()]) # 3-d
        ans = least_squares(fun=self.__f_lsq, x0=a0, bounds=bnds)
        print('Best Coef =', ans.x)
        return ans.x


    def f(self, AB:np.ndarray):
        res = 0
        for i in range(1, self.n):
            tmp = self.ax1[i] + AB[0] * self.x0[i] + AB[1] * self.z[i] - AB[2]
            res += (tmp ** 2)
        return res


    def __pso(self, bnds=[(-100, 100), (-100, 100), (-100, 100)]):
        ''' Particle Swarm Optimize Algorithm '''
        n = 2  # demensions 维数
        N, niter = 50, 500
        vmin, vmax = -1, 1
        w, c1, c2 = 1, 2, 2.1
        c = c1 + c2
        K = 2 / (np.abs(2 - c - np.sqrt(c * c - 4 * c)))
        def f(x:np.ndarray):
            y = self.f(x)
            penalty = 0x3f3f3f3f
            for i in range(n):
                tmp1, tmp2 = bnds[i][0] - x[i], x[i] - bnds[i][1]
                if tmp1 > 0:
                    y += (tmp1 * penalty)
                if tmp2 > 0:
                    y += (tmp2 * penalty)
            return y
        x, v = rand(N, n), rand(N, n)  # 注意初始值X要在取值范围内随机投点
        y = np.array([f(v) for v in x])
        pbest_x, pbest_y = x.copy(), y.copy()
        gbest_x, gbest_y = x[y.argmin()], y.min()
        for _ in range(niter):
            for i in range(N):
                for j in range(n):
                    pb = c1 * rand(1) * (pbest_x[i][j] - x[i][j])
                    gb = c2 * rand(1) * (gbest_x[j] - x[i][j])
                    v[i][j] = K * (v[i][j] + pb + gb)
                    v[i][j] = min(v[i][j], vmax)
                    v[i][j] = max(v[i][j], vmin)
                x[i] += v[i]
                y[i] = f(x[i])
                if y[i] < pbest_y[i]:
                    pbest_x[i], pbest_y[i] = x[i], y[i]
                if y[i] < gbest_y:
                    gbest_x, gbest_y = x[i], y[i]
        print("Global Coef = {0}, Cost = {1:.6f}".format(gbest_x, gbest_y))
        return gbest_x


    def __dual_annel(self, bnds=[(-100, 100), (-100, 100), (-100, 100)]):
        ''' dual annealing algorithm '''
        ans = DA(func=self.f, bounds=bnds, maxiter=1000, seed=623)
        print("Global Coef = {0}, Cost = {1:.6f}".format(ans.x, ans.fun))
        return ans.x


    def __diff_evol(self, bnds=[(-100, 100), (-100, 100), (-100, 100)]):
        ''' differential evolution algorithm '''
        ans = DE(func=self.f, bounds=bnds, maxiter=1000, popsize=25,
                    mutation=(0.5, 1), recombination=0.7, tol=0.001)
        print("Global Coef = {0}, Cost = {1:.6f}".format(ans.x, ans.fun))
        return ans.x


    def ode(self, t, coef):
        ''' 根据参数coef利用MATLAB求解常微分方程
        x'' + a1*x' + a2*x = b
        x(0)=v1, x(n-1)=v2
        的解析解
        '''
        y = 203.85 * exp(0.22622 * t) - 0.5324 * exp(0.86597 * t) - 162.317
        return y


    def run(self):
        self.__process_data()
        #a, b = self.__lsq() # 采用最小二乘拟合参数
        #a, b = self.__pso()  # 采用粒子群算法拟合参数
        #a, b = self.__dual_annel()  # 采用双适应度模拟退火算法拟合参数
        coef = self.__diff_evol() # 采用差分进化算法拟合参数
        '''计算得到参数后使用MATLAB求解白化的二阶常微分方程'''
        err = zeros(shape=self.x0.shape).astype(np.float)  # 残差
        for i in range(0, self.m):
            tmp = self.ode(i, coef)
            self.x1_p[i] = tmp
        for i in range(1, self.m):
            self.x0_p[i] = self.x1_p[i] - self.x1_p[i - 1]
        for i in range(1, self.n):
            err[i] = abs((self.x0[i] - self.x0_p[i]) / self.x0[i])
        # 残差检验
        print("残差Error", err)
        if err.all() < 0.1:
            print("残差检验达到较高要求(<0.1)")
        elif err.all() < 0.2:
            print("残差检验通过一般要求(<0.2)")
        print("******原始数据为******")
        print(self.x0)
        print("******预测为******")
        print(self.x0_p[:-(self.m - self.n)])
        print("******" + "接下来" + str(self.m - self.n) + "期预测为******")
        print(self.x0_p[self.n:])


# demo1
data = [41, 49, 61, 78, 96, 104]
gm11 = GM_11(data=data, nxt=4)
gm11.run()


