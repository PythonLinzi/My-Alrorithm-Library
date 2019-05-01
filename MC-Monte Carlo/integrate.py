import numpy as np
import matplotlib.pyplot as plt

N=100000
squareS=9*12
points=[[xy[0]*12,xy[1]*9] for xy in np.random.rand(N,2)]

x=np.linspace(0,12)
y1=x**2
y2=12-x

plt.plot(x,y1)
plt.fill_between(x,y1,where=(y1>0),color='red',alpha=0.5)
plt.plot(x,y2)
plt.fill_between(x,y2,where=(y2>0),color='blue',alpha=0.5)
plt.scatter([xy[0] for xy in points],[xy[1] for xy in points],s=5,c=np.random.rand(N),alpha=0.01)
plt.show()

count=0
for xy in points:
    if xy[0]<3:
        if xy[1]<=xy[0]**2:
            count+=1
    else:
        if xy[1]<=12-xy[0]:
            count+=1

s=count/N*squareS
print("s=%f\n"%(s))