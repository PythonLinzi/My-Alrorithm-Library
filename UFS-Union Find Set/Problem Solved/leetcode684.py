class Solution:
    def findRedundantConnection(self, edges: "List[List[int]]") -> "List[int]":
        pre = [i for i in range(len(edges) + 1)]

        def find(x:int) -> int:
            root = x
            while pre[root] != root:
                root = pre[root]
            now = x
            while now != root:
                nxt = pre[now]
                pre[now] = root
                now = nxt
            return root

        for u, v in edges:
            ru, rv = find(u), find(v)
            if ru != rv:
                pre[ru] = rv
            else:
                return [u, v]


if __name__ == '__main__':
    s = Solution()
    e = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    print(s.findRedundantConnection(e))
