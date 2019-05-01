import numpy as np
import datetime


def floyd(graph):
    '''Floyd Algorithm'''
    '''Floyd不能处理带有'负权回路'的图'''
    d = np.array(graph)
    inf = int(1e9)
    n = len(graph)
    for i in range(0, n):
        for j in range(0, n):
            d[i][j] = inf if d[i][j] == 0 else d[i][j]
    for i in range(0, n): d[i][i] = 0
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


if __name__=='__main__':
    g = [[0,1,12,0,0,0], [1,0,9,3,0,0], [12,9,0,4,5,0],
         [0,3,4,0,13,15], [0,0,5,13,0,4], [0,0,0,15,4,0]]
    s = datetime.datetime.now()
    dis = floyd(g)
    e = datetime.datetime.now()
    print(dis)
    print(e - s)
