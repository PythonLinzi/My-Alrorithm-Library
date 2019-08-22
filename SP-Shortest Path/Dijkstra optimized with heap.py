import heapq


def dijkstra(graph, S:int):
    ''' Dijkstra Algorithm '''
    inf = 0x3f3f3f3f
    dis = dict((key, inf) for key in graph)
    vis = dict((key, False) for key in graph)
    path = dict((key, [S]) for key in graph)  # Path Record
    dis[S], pq = 0, []
    heapq.heappush(pq, [dis[S], S])
    while len(pq) > 0:
        v_dis, v = heapq.heappop(pq)
        if vis[v] == True:
            continue
        vis[v] = True
        p = path[v].copy()
        for node in graph[v]:
            new_dis = dis[v] + float(graph[v][node])
            if new_dis < dis[node] and (not vis[node]):
                dis[node] = new_dis
                heapq.heappush(pq, [dis[node], node])
                tmp = p.copy()
                tmp.append(node)
                path[node] = tmp
    return dis, path


def print_sp(dis:dict, path:dict, S:int):
    s = str(S)
    print('******Distance******')
    for k, v in dis.items():
        print(s + '->' + str(k) + " length = %.1f" % v)
    print('******Path******')
    for k, v in path.items():
        print(s + '-->' + str(k), end=': ')
        n = len(v)
        for i in range(n - 1):
            print(str(v[i]), end='->')
        print(str(v[-1]))
    return


if __name__ == '__main__':
    G = {1: {1: 0, 2: 10, 4: 30, 5: 100},
         2: {2: 0, 3: 50},
         3: {3: 0, 5: 10},
         4: {3: 20, 4: 0, 5: 60},
         5: {5: 0},
         }
    S = 1
    distance, path = dijkstra(G, S=S)
    print_sp(distance, path, S)

'''
******Distance******
1->1 length = 0.0
1->2 length = 10.0
1->3 length = 50.0
1->4 length = 30.0
1->5 length = 60.0
******Path******
1-->1: 1
1-->2: 1->2
1-->3: 1->4->3
1-->4: 1->4
1-->5: 1->4->3->5
'''
