class Dinic:
    '''Dinic Minimum Cost Maximum Flow Algorithm'''
    class Edge:
        def __init__(self, to:int, pre:int, flow:int, cost:int):
            self.to, self.pre = to, pre
            self.flow, self.cost = flow, cost


    def __init__(self):
        self.maxn, self.INF = 1000005, 0x3f3f3f3f
        self.maxFlow, self.minCost = 0, 0
        self.vis = [False for _ in range(self.maxn)]
        self.len = 1
        self.dis = [self.INF for _ in range(self.maxn)]
        self.last = [0 for _ in range(self.maxn)]
        self.S, self.T = 1, 0
        self.edge = [self.Edge(0, 0, 0, 0), self.Edge(0, 0, 0, 0)]


    def add(self, from_:int, to:int, flow:int, cost:int):
        self.len += 1
        self.edge.append(self.Edge(to, self.last[from_], flow, cost))
        self.last[from_] = self.len
        self.len += 1
        self.edge.append(self.Edge(from_, self.last[to], 0, -cost))
        self.last[to] = self.len


    def __SPFA(self) -> bool:
        self.vis = [False for _ in range(self.maxn)]
        self.dis = [self.INF for _ in range(self.maxn)]
        q, self.dis[self.T], self.vis[self.T] = [self.T], 0, True
        while q:
            now = q.pop(0)
            self.vis[now] =False
            i = self.last[now]
            while i:
                to = self.edge[i].to
                if self.edge[i ^ 1].flow > 0 \
                        and self.dis[to] > self.dis[now] - self.edge[i].cost:
                    self.dis[to] = self.dis[now] - self.edge[i].cost
                    if not self.vis[to]:
                        q.append(to)
                        self.vis[to] = True
                i = self.edge[i].pre
        return self.dis[self.S] != self.INF


    def __DFS(self, u:int, flow:int) -> int:
        self.vis[u] = True
        if u == self.T:
            return flow
        used = 0
        i = self.last[u]
        while i:
            v = self.edge[i].to
            if not self.vis[v] \
                    and self.dis[v] == self.dis[u] - self.edge[i].cost \
                    and self.edge[i].flow != 0:
                minFlow = self.__DFS(v, min(self.edge[i].flow, flow - used))
                if minFlow != 0:
                    self.minCost += (minFlow * self.edge[i].cost)
                    used += minFlow
                    self.edge[i].flow -= minFlow
                    self.edge[i ^ 1].flow += minFlow
                if flow == used:
                    break
            i = self.edge[i].pre
        return used


    def main(self, S:int, T:int):
        self.S, self.T = S, T
        self.maxFlow, self.minCost = 0, 0
        while self.__SPFA():
            self.vis[T] = True
            while self.vis[T]:
                self.vis = [False for _ in range(self.maxn)]
                self.maxFlow += self.__DFS(S, self.INF)
        print('Maximum Flow:', self.maxFlow)
        print('Minimum Cost:', self.minCost)
        return self.maxFlow, self.minCost


if __name__ == '__main__':
    edge = [[1, 2, 8, 2], [1, 4, 7, 8], [2, 4, 5, 5],
            [2, 3, 9, 2], [3, 4, 2, 1], [4, 5, 9, 3],
            [5, 3, 6, 4], [3, 6, 5, 6], [5, 6, 10, 7]]
    # edge[[from, to, maxflow, cost]]
    dinic = Dinic()
    for u, v, f, c in edge:
        dinic.add(u, v, f, c)
    dinic.main(S=1, T=6)
