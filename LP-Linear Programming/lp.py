'''
maximize z = 2*x1+3*x2-5*x3
x1+x2+x3 = 7
2*x1-5*x2+x3>=10
x1+3*x2+x3<=12
x1,x2,x3>=0
'''

from scipy import optimize as op
import numpy as np

coef = np.array([2,3,-5])
# 不等式条件限制, 若无限制则不填
A_ub = np.array([[-2,5,-1],[1,3,1]])
B_ub = np.array([-10,12])
# 等式条件限制, 若无限制则对应位置不填（即None）
A_eq = np.array([[1,1,1]])
B_eq = np.array([7])

x1 = (0,7)
x2 = (0,7)
x3 = (0,7)

#ans=op.linprog(coef, A_ub, B_ub, A_eq, B_eq, bounds=(x1, x2, x3))
ans=op.linprog(coef, A_ub, B_ub, A_eq, B_eq)
print(ans)

'''
     fun: -13.999999999999998 # 最小值，取相反数即为最大值
 message: 'Optimization terminated successfully.'
     nit: 3
   slack: array([5., 4., 7., 3., 0.])
  status: 0
 success: True
       x: array([3., 0., 4.]) # 此时x1,x2,x3的取值

'''