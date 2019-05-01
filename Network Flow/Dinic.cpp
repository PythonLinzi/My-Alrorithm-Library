#include <iostream>
#include <cstring>
#include <queue>
#include <vector>
#include <algorithm>
using namespace std;

const int N = 10005, M = 20005, INF = 0x3f3f3f3f;
int n, m, x, y, weight, idx = 0;
int w[M * 2], nxt[M * 2], dis[N], S = 1, T, ans = 0;
vector<int> g[N];//存储边的序号


bool BFS()
{
    memset(dis, 0, sizeof(dis));
    queue<int> q;
    q.push(S);
    dis[S] = 1;
    while (!q.empty()){
        int from = q.front();
        q.pop();
        for (int i = 0; i < g[from].size(); ++i) {
            int to = g[from][i];
            if (!dis[nxt[to]] && w[to]){
                q.push(nxt[to]);
                dis[nxt[to]] = dis[from] + 1;
            }
        }
    }
    return bool(dis[T]);
}


int Dinic(int u, int flow)
{
    if (u == T)
        return flow;
    for (int i = 0; i < g[u].size(); ++i) {
        int to = g[u][i];
        if (dis[nxt[to]] == dis[u] + 1 && w[to]){
            int minFlow = Dinic(nxt[to], min(flow, w[to]));
            if (minFlow){
                w[to] -= minFlow;
                w[to ^ 1] += minFlow;
                return minFlow;
            }
        }
    }
    return 0;
}



int main()
{
    ios_base::sync_with_stdio(false);
    cin >> m >> n;
    S = 1, T = n;
    for (int i = 0; i < m; ++i) {
        cin >> x >> y >> weight;
        w[idx] = weight;
        nxt[idx] = y;
        g[x].push_back(idx++);
        w[idx] = 0;
        nxt[idx] = x;
        g[y].push_back(idx++);
    }//create graph
    while (BFS())
        ans += Dinic(S, INF);
    cout << "Maximum Flow: " << ans << endl;
    return 0;
}
