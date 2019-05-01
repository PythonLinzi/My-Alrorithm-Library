n, m = 6, 9
pre = [i for i in range(n + 1)]
rank = [0 for i in range(n + 1)]

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


def union(x:int, y:int):
    rx, ry = find(x), find(y)
    if rank[rx] < rank[ry]:
        pre[rx] = ry
    elif rank[rx] > rank[ry]:
        pre[ry] = rx
    else:
        pre[rx] = ry
        rank[ry] += 1
    return


g = [[0, 16, 13, 0, 0, 0],
     [0, 0, 0, 12, 0, 0],
     [0, 4, 0, 0, 14, 0],
     [0, 0, 9, 0, 0, 20],
     [0, 0, 0, 7, 0, 4],
     [0, 0, 0, 0, 0, 0]]
for i in range(len(g)):
    for j in range(len(g[0])):
        if g[i][j]:
            union(i, j)
idx = pre[0]
cnt = 1
for i in range(len(g)):
    if pre[i] != idx:
        cnt += 1
print(cnt)