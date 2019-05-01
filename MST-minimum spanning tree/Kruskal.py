class Kruskal:
    '''Kruskal algorithm for MST'''
    def __init__(self, n:int, edge:"List[List[int]]"):
        self.m = len(edge)  #  the number of edges
        self.e = edge  #  the set composed of edges
        self.n = n  #  the number of vertices
        self.pre = [i for i in range(n + 1)]
        self.rank = [0 for i in range(n + 1)]
        self.ans = []
        self.sum = 0


    def find(self, x:int) -> int:
        root = x
        while self.pre[root] != root:
            root = self.pre[root]
        now = x
        while now != root:
            '''compress path'''
            nxt = self.pre[now]
            self.pre[now] = root
            now = nxt
        return root


    def union(self, x:int, y:int):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.pre[rx] = ry
            self.rank[ry] += 1
        else:
            self.pre[ry] = rx
            self.rank[rx] += 1

    def merge(self, x:int, y:int):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.pre[rx] = ry


    def kruskal(self):
        e = sorted(self.e, key=lambda x: x[-1])
        cnt = 0
        for u, v, w in e:
            if self.find(u) != self.find(v):
                self.sum += w
                self.union(u, v)
                self.ans.append([u, v, w])
                cnt += 1
            if cnt == self.n - 1:
                break
        return self.ans


    def print_ans(self):
        print('Minimum Spanning Tree:')
        for u, v, w in self.ans:
            print(str(u) + '<-->'+ str(v) + ' {weight: ' + str(w) + '}')
        print("Minimum cost:", self.sum)


if __name__ == '__main__':
    n, m = 6, 12
    edge = [[1, 2, 3], [1, 3, 2], [2, 3, 2], [2, 4, 4],
            [3, 5, 9], [3, 4, 9], [4, 5, 9], [1, 5, 8],
            [2, 6, 4], [3, 6, 4], [4, 6, 6], [5, 6, 7]]
    #  edge = [u, v, w]
    kr = Kruskal(n, edge)
    kr.kruskal()
    kr.print_ans()
