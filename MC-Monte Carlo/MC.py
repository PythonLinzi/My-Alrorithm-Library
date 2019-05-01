#!/usr/bin/python
#-*- coding:UTf-8 -*-
import numpy as np
import datetime

def integrate(f,a,b,low,high):
    T=np.ceil(b-a)*1000
    x=np.linspace(a,b,T)
    all=(high-low)*(b-a)
    count=0;n=int(1e6)
    points=np.array([[xy[0]*(b-a)+a,xy[1]*(high-low)+low] for xy in np.random.rand(n,2)])
    for xy in points:
        if xy[1]<f(xy[0]):
            count+=1
    ans=all*(count/n)
    return ans

def cal_pi():
    n=int(1e6)
    points=np.array([[xy[0]*2,xy[1]*2] for xy in np.random.rand(n,2)])
    cnt=0
    for xy in points:
        if (xy[0]-1)**2+(xy[1]-1)**2<=1:
            cnt+=1
    ans=4*cnt/n
    return ans


if __name__=='__main__':
    #case1:
    def f(x):
        return x*x
    a = 1;b = 2
    low = 0;high = f(2)
    start = datetime.datetime.now()
    area = integrate(f, a, b, low, high)
    end = datetime.datetime.now()
    print('case1:s=',area,'time used:',end-start)

    #case2:
    def g(x):
        return np.log(x)*np.log(x)
    start = datetime.datetime.now()
    low = g(a);high = g(2)
    area = integrate(g, a, b, low, high)
    end = datetime.datetime.now()
    print('case2:s=',area, 'time used:', end - start)

    start=datetime.datetime.now()
    PI=cal_pi()
    end=datetime.datetime.now()
    print("pi is about:",PI,'time used:',end-start)
    '''
    case1:s= 2.3311 time used: 0:00:02.403535
    case2:s= 0.1886844685319839 time used: 0:00:04.491985
    pi is about: 3.142452 time used: 0:00:02.964073
    '''
