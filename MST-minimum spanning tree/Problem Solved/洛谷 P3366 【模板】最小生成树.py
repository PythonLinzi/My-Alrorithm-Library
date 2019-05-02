N, M = 5005, 200005
pre = [i for i in range(N)]
rank = [0 for i in range(N)]


def find(x: int) -> int:
    root = x
    while root != pre[root]:
        root = pre[root]
    now = x
    while now != root:
        nxt = pre[now];
        pre[now] = root
        now = nxt
    return root


def unite(x: int, y: int):
    fx, fy = find(x), find(y)
    if fx == fy:
        return
    if rank[fx] > rank[fy]:
        pre[fy] = fx
        rank[fx] += 1
    else:
        pre[fx] = fy
        rank[fy] += 1
    return


def kruskal(n:int, m:int, edge:'List[List[int]]'):
    e = sorted(edge, key=lambda x: x[-1])
    ans, cnt = 0, 0
    for u, v, w in e:
        if find(u) != find(v):
            ans += w
            unite(u, v)
            cnt += 1
        if cnt == n - 1:
            break
    if cnt < n - 1:
        return -1
    return ans


fail = 'orz'
n, m = map(int, input().split())
edge = []
for i in range(m):
    u, v, w = map(int, input().split())
    edge.append([u, v, w])
ans = kruskal(n, m, edge)
if ans:
    print(ans)
else:
    print(fail)


