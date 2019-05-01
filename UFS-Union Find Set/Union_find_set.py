
class Ufs:
    ''' Union Find Set algorithm '''
    def __init__(self, graph:"List[List[int]]"):
        self.n = len(graph)
        self.pre = [i for i in range(self.n + 1)]
        self.rank = [0 for _ in range(self.n + 1)]


    def find(self, x:int) -> int:
        root = x
        while self.pre[root] != root:
            root = self.pre[root]
        now = x
        while now != root:
            ''' compress path '''
            nxt = self.pre[now]
            self.pre[now] = root
            now = nxt
        return root

    def union(self, x:int, y:int):
        fx, fy = self.find(x), self.find(y)
        if fx == fy:
            return
        if self.rank[fx] < self.rank[fy]:
            self.pre[fx] = fy
            self.rank[fy] += 1
        else:
            self.pre[fy] = fx
            self.rank[fx] += 1

    def merge(self, x:int, y:int):
        fx, fy = self.find(x), self.find(y)
        if fx != fy:
            self.pre[fx] = fy


