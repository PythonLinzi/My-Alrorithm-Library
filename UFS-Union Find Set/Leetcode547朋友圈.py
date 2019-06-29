class Solution:
    def findCircleNum(self, M: 'List[List[int]]') -> 'int':
        n = len(M)
        pre, rank = [i for i in range(n)], [0 for i in range(n)]
        def find(x:int) -> int:
            root = x
            while pre[root] != root:
                root = pre[root]
            i = x
            while pre[i] != root:
                tmp = pre[i]
                pre[i] = root
                i = tmp
            return root
        def union(x:int, y:int):
            rx, ry = find(x), find(y)
            if rank[rx] > rank[ry]:
                pre[ry] = rx
                rank[rx] += 1
            else:
                pre[rx] = ry
                rank[ry] += 1
        for i in range(n):
            for j in range(n):
                if M[i][j] == 1:
                    union(i, j)
        ans = 0
        for i in range(n):
            if pre[i] == i:
                ans += 1
        return ans


if __name__ == '__main__':
    m = [[1,1,0],[1,1,0],[0,0,1]]
    s = Solution()
    print(s.findCircleNum(m))
