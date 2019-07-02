import numpy as np
from scipy.integrate import quad, dblquad, tplquad


'''一重积分 one-dementional integrate'''
f = lambda x: np.sin(x)
ans, err = quad(func=f, a=0, b=np.pi)
print(ans, err)


'''二重积分 two-dementional integrate'''
g = lambda x, y: np.sin(x) * np.cos(y)
ans1, err1 = dblquad(func=g, a=0, b= np.pi, gfun=lambda x:x ** 2, hfun=lambda x:2 * x)
# func被积分函数, a--x的积分下界, b--x的积分上界, gfun--y的下界, hfunc--y的上界
print(ans1, err1)


'''三重积分 cubic integrate'''
ans2, err2 = tplquad(lambda z,y,x:1/(np.sqrt(x+y**2+z**3)),#函数
                0,#x下界0
                1,#x上界1
                lambda x:-x,#y下界-x
                lambda x:x,#y上界x
                lambda x,y:np.sin(x),#z下界sin(x)
                lambda x,y:x+2*y)#z上界x+2*y
print (ans2, err2)
