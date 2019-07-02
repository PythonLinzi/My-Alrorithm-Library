import numpy as np
import matplotlib.pyplot as plt

class PolyFit ():
    ''' polynomial fitting algorithm '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.degree = 0
        self.coef = None
        self.f = None
        self.MSE = 0
        self.fig = plt.figure()

    def fit(self, degree):
        self.degree = degree
        # 根据已有点训练得多项式参数,三个参数分别为x, y, 多项式最高项次数
        self.coef = np.polyfit(self.x, self.y, self.degree) # 系数
        # 多项式函数对象
        self.f = np.poly1d(self.coef)

        e = np.abs(self.y - np.polyval(self.f, self.x))
        self.MSE = np.sum(np.power(e, 2) / len(self.x))  # var error
        return self.coef, self.f

    def get_error(self):
        return self.MSE

    def show(self):
        plt.plot(self.x, self.y, 'ro-', markersize = 2,
                 figure = self.fig, label = 'orginal')
        plt.plot(self.x, np.polyval(self.f, self.x), 'b*-', markersize = 1,
                 figure = self.fig, label = 'polyfit')
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Polyfit Figure')
        #plt.savefig('figure.png')
        plt.show()

    def predict(self, x0):
        return np.polyval(self.f, x0)



if __name__ == '__main__':
    x = np.linspace(1,10,1000)
    y = np.sin(x)

    fitting = PolyFit(x, y)
    coef, f = fitting.fit(9)
    print('coef:', str(coef))
    print('error:', fitting.MSE)
    print('x1 =', np.pi, 'y1 = sin(x1) =', fitting.predict(np.pi))

    fitting.show()

