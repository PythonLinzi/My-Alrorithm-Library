# !/bin/usr/python
# -*- coding: UTF-8 -*-

import numpy as np

N=10000000
points=[[x[0]*100,x[1]*100,x[2]*100,x[3]*100,x[4]*100] for x in np.random.rand(N,5)]

def f(x):
	return (x[0]**2+x[1]**2+3*x[2]**2+4*x[3]**2+2*x[4]**2-8*x[0]-2*x[1]-3*x[2]-x[3]-2*x[4])

def ok(x):
	flag=0
	sum1=sum(x)
	if sum1<=400:
		flag+=1
	sum2=sum(x)+x[1]+x[2]+5*x[4]
	if sum2<=800:
		flag+=1
	sum3=x[0]*2+x[1]+6*x[2]
	if sum3<=200:
		flag+=1
	sum4=x[2]+x[3]+5*x[4]
	if sum4<=200:
		flag+=1
	if flag==4:
		return True
	else:
		return False

re=0
decision=[]
for x in points:
	if ok(x):
		temp=f(x)
		if temp>re:
			re=temp
			for i in x:
				decision.append(i)

print("Best answer is "+str(re))

#actually best answer is 51568
#as N is bigger, the answer is more acurate
#when N=100W, acuration is about 98.4%