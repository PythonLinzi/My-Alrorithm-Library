class Dinic:
    '''Dinic algorithm'''
    def __init__(self, V:int, E:int, graph:'List[List[int]]', S:int, T:int):
        self.n, self.m = V, E  # V = |Vertices|, E = |Edges|
        self.S, self.T = S, T
        self.w = [0 for _ in range(2 * (E + 1))]
        self.nxt = [0 for _ in range(2 * (E + 1))]
        self.g = [[] for _ in range(V + 1)]
        idx = 0
        for u, v, w in graph:
            self.w[idx] = w
            self.nxt[idx] = v
            self.g[u].append(idx)
            idx += 1
            self.w[idx] = 0
            self.nxt[idx] = u
            self.g[v].append(idx)
            idx += 1
        self.dis = None
        self.ans = 0


    def BFS(self) -> bool:
        self.dis = [0 for _ in range(self.n + 1)]
        self.dis[self.S], q = 1, [self.S]
        while q:
            now = q.pop(0)
            for to in self.g[now]:
                if not self.dis[self.nxt[to]] and self.w[to]:
                    q.append(self.nxt[to])
                    self.dis[self.nxt[to]] = self.dis[now] + 1
        return bool(self.dis[self.T])


    def DFS(self, u:int, flow:int):
        if u == self.T:
            return flow
        for to in self.g[u]:
            if self.dis[self.nxt[to]] == self.dis[u] + 1 and self.w[to]:
                minFlow = self.DFS(self.nxt[to], min(flow, self.w[to]))
                if minFlow:
                    self.w[to] -= minFlow
                    self.w[to ^ 1] += minFlow
                    return minFlow
        return 0


    def dinic(self):
        sum, inf = 0, int(1e9)
        while self.BFS():
            sum += self.DFS(self.S, inf)
        print("Maximum Flow:", sum)


if __name__ == '__main__':
    n, m = 6, 9
    g = [[1, 2, 16], [1, 3, 13], [3, 2, 4],
         [2, 4, 12], [4, 3, 9], [3, 5, 14],
         [5, 4, 7], [4, 6, 20], [5, 6, 4]]
    dinic = Dinic(n, m, g, 1, n)
    dinic.dinic()
