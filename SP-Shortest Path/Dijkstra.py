import numpy as np
import datetime


def dijkstra(graph, node) -> list:
    '''Dijkstra Algorithm'''
    '''weight must >= 0'''
    inf = int(1e9)
    g = np.array(graph)
    n = len(g)
    d = np.repeat(inf, n)
    visit = np.repeat(False, n).astype(np.bool)
    for i in range(0, n):
        for j in range(0, n):
            g[i][j] = inf if g[i][j] == 0 else g[i][j]
    for i in range(0, n):
        d[i] = g[node][i]
    visit[node] = True
    d[node] = 0
    for i in range(0, n):
        tmp = inf
        u = node
        for j in range(0, n):
            if not visit[j] and d[j] < tmp:
                tmp = d[j]
                u = j
        visit[u] = True
        for j in range(0, n):
            if not visit[j]:
                d[j] = min(d[j], d[u] + g[u][j])
    return d


if __name__ == '__main__':
    graph = [[0, 1, 12, 0, 0, 0], [1, 0, 9, 3, 0, 0],
             [12, 9, 0, 4, 5, 0],[0, 3, 4, 0, 13, 15],
             [0, 0, 5, 13, 0, 4], [0, 0, 0, 15, 4, 0]]
    dis = []
    start = datetime.datetime.now()
    for i in range(0, len(graph)):
        dis = dijkstra(graph, i)
        print(dis)
    end = datetime.datetime.now()
    print(end - start)
