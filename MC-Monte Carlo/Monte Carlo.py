# !/bin/usr/python
# -*- coding: UTF-8 -*-

#integrate of x^3 in (0,2)

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

N=100000
points=[[xy[0]*2,xy[1]*8] for xy in np.random.rand(N,2)]

x=np.linspace(0,2)
y=x**3
plt.plot(x,y)
plt.fill_between(x,y,where=(y>0),color='blue',alpha=0.5)
plt.scatter([xy[0] for xy in points],[xy[1] for xy in points],s=3,color='red',alpha=0.1)

count=0
for xy in points:
	if xy[1]<=xy[0]**3:
		count+=1

print("count="+str(count))
s=count/N*2*8
print("s=%f"%(s))

realS=quad(lambda x:x**3,0,2)[0]
print("real s is "+str(realS))

delta=s/realS
print("delta="+str(delta*100)+"%")

plt.show()