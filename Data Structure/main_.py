class Solution:
    def networkDelayTime(self, times: list, N: int, K: int) -> int:
        inf = int(1e9)
        g = [[int(1e9)] * N for _ in range(N)]
        for item in times:
            g[item[0] - 1][item[1] - 1] = item[2]

        n = len(g)
        v = [False for _ in range(n)]
        d = [inf for _ in range(n)]
        node = K - 1
        for i in range(0, n):
            g[i][i] = 0
            d[i] = g[node][i]
        v[node] = True
        d[node] = 0
        for i in range(n):
            tmp = inf
            u = node
            for j in range(n):
                if not v[j] and d[j] < tmp:
                    tmp = d[j]
                    u = j
            v[u] = True
            for j in range(n):
                if not v[j]:
                    d[j] = min(d[j], d[u] + g[u][j])
        for i in range(n):
            if d[i] == inf:
                return -1
        ans = max(d)
        return ans


if __name__ == '__main__':
    network = [[3,5,78],[2,1,1],[1,3,0],[4,3,59],[5,3,85],
               [5,2,22],[2,4,23],[1,4,43],[4,5,75],[5,1,15],
               [1,5,91],[4,1,16],[3,2,98],[3,4,22],[5,4,31],
               [1,2,0],[2,5,4],[4,2,51],[3,1,36],[2,3,59]]
    s = Solution()
    print(s.networkDelayTime(network, 5, 5))
