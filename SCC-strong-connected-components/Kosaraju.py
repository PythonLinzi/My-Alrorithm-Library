class Kosaraju:
    ''' Kosaraju algorithm for strong connected component '''
    def __init__(self, graph):
        '''
        graph is adjacency matrix,
        if graph is adjacency table,
        then plaese adjust the code_#1
        '''
        self.g, self.gt = self.process(graph) #1
        self.stack, self.catagory = [], []
        self.n = len(self.g)
        self.v, self.vt = [False] * self.n, [False] * self.n


    def process(self, graph:'List[List[int]]'):
        ''' return adjacency table '''
        n = len(graph)
        g, gt = [[] for _ in range(n)], [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if graph[i][j] == 1:
                    g[i].append(j)
                    gt[j].append(i)
        return g, gt


    def dfs(self, idx:int):
        for i, x in enumerate(self.g[idx]):
            if not self.v[x]:
                self.v[x] = True
                self.dfs(x)
        self.stack.append(idx)


    def dfs_t(self, idx:int, label:int):
        self.catagory[label - 1].add(idx + 1)
        for i, x in enumerate(self.gt[idx]):
            if not self.vt[x]:
                self.vt[x] = True
                self.dfs_t(x, label)


    def main_loop(self) -> 'List[Set[int]]':
        for i in range(self.n):
            if not self.v[i]:
                self.v[i] = True
                self.dfs(i)
        label = 0
        while self.stack:
            idx = self.stack[-1]
            if not self.vt[idx]:
                self.vt[idx] = True
                label += 1
                tmp = set()
                self.catagory.append(tmp)
                self.dfs_t(idx, label)
            self.stack.pop()
        return self.catagory



if __name__ == '__main__':
    g = [[0, 1, 1, 0], [0, 0, 0, 0], [0, 1, 0, 1], [1, 0, 0, 0]]
    gg = [[0, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 1, 0],
          [1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0]]
    kosaraju = Kosaraju(gg)
    print(kosaraju.main_loop())