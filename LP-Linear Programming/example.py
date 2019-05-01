'''
max f1=-3*x1+2*x2
max f2=4*x1+3*x2
s.t.
2*x1+3*x2<=18
2*x1+x2<=10
x1,x2>=0
'''

from scipy import optimize as op
import numpy as np

coef1 = np.array([3,-2])
coef2 = np.array([-4,-3])

a_ub = np.array([[2,3],[2,1]])
b_ub = np.array([18,10])

a_eq = None
b_eq = None

bounds = None

f1 = op.linprog(coef1, a_ub, b_ub)
f2 = op.linprog(coef2, a_ub, b_ub)

min_f1 = -f1.fun; x_f1 = f1.x
min_f2 = -f2.fun; x_f2 = f2.x
print("Min f1: "+str(min_f1)," x: "+str(x_f1))
print("Min f2: "+str(min_f2)," x: "+str(x_f2))

'''
Min f1: 12.0  x: [0. 6.]
Min f2: 24.0  x: [3. 4.]
'''