class Tarjan:
    ''' Tarjan algorithm for strong connected component '''
    def __init__(self, graph:'List[List[int]]'):
        self.g = graph
        self.length = len(self.g)
        self.dfn, self.low = [0] * self.length, [0] * self.length
        self.stack, self.is_in_stack = [], [False] * self.length
        self.cnt, self.number = 0, 0
        self.ans = []


    def tarjan_(self, u:int):
        self.cnt += 1
        self.stack.append(u)
        self.is_in_stack[u] = True
        self.low[u] = self.dfn[u] = self.cnt
        for v in range(self.length):
            if self.g[u][v]:
                if not self.dfn[v]:
                    self.tarjan_(v)
                    self.low[u] = min(self.low[u], self.low[v])
                elif self.is_in_stack[v]:
                    self.low[u] = min(self.low[u], self.dfn[v])
        if self.dfn[u] == self.low[u]:
            self.number += 1
            tmp = set()
            j = -1
            while j != u:
                j = self.stack[-1]
                tmp.add(j + 1)
                self.stack.pop()
                self.is_in_stack[j] = False
            self.ans.append(tmp)


    def run_tarjan(self):
        self.tarjan_(0)
        for s in self.ans:
            print(s)


if __name__ == '__main__':
    gg = [[0, 1, 1, 0], [0, 0, 0, 0], [0, 1, 0, 1], [1, 0, 0, 0]]
    g = [[0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0],
         [1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]
    tar = Tarjan(g)
    tar.run_tarjan()