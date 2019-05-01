class Ford_Fulkerson:
    '''Ford_Fulkerson algorithm'''
    def __init__(self, V:int, E:int, graph:'List[List[int]]'):
        self.g, self.ans = graph, 0
        self.n, self.m = V, E # V = |Vertices|, E = |Edges|


    def ford_fulkerson(self):
        n = self.n
        while True:
            v = [False for _ in range(n)]
            pre = [-1 for _ in range(n)]
            now = 0
            from collections import deque
            q, v[now] = deque(), True
            q.append(0)
            while q: #  BFS:search augmentation path
                now = q.popleft()
                if now == n - 1:
                    break
                for i in range(n):
                    if self.g[now][i] and (not v[i]):
                        q.append(i)
                        v[i] = True
                        pre[i] = now
            if not v[n - 1]: #  if no more augmentation path
                break
            minP = int(1e9)
            u = n - 1
            while u:
                minP = min(minP, self.g[pre[u]][u])
                u = pre[u]
            u = n - 1
            while u:
                self.g[pre[u]][u] -= minP
                self.g[u][pre[u]] += minP
                u = pre[u]
            self.ans += minP


    def print_ans(self):
        print('Maximum Flow:', self.ans)


if __name__ == '__main__':
    g = [[0, 16, 13, 0, 0, 0],
         [0, 0, 0, 12, 0, 0],
         [0, 4, 0, 0, 14, 0],
         [0, 0, 9, 0, 0, 20],
         [0, 0, 0, 7, 0, 4],
         [0, 0, 0, 0, 0, 0]]
    ford = Ford_Fulkerson(6, 9, g)
    ford.ford_fulkerson()
    ford.print_ans()
