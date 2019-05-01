#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
#include <vector>
#include <iomanip>
#define maxn 1000005
using namespace std;

/*
 * S -> vehicles -> workers -> T
 * S = 0, T = n + m * n +1
 * node 1 ~ n denote vehicles
 * node n + 1 ~ m * n + n denote workers
 * there must be a vehicles' repair sequence
 * j * n + k denote that worker_j repair the vehicle which is repaired k_th
 */


class Dinic
{
    struct Edge{int to, pre, flow, cost;};
    struct Data{int maxFlow, minCost;};
    Edge edge[maxn];
    Data ans;
    int dis[maxn], len = 1, last[maxn], S, T, INF = 0X3f3f3f3f;
    bool vis[maxn];

    bool SPFA(){
        memset(vis, false, sizeof(vis));
        memset(dis, 0x3f, sizeof(dis));
        queue<int> q;
        q.push(T);
        dis[T] = 0, vis[T] = 1;
        while (!q.empty()){
            int now = q.front();
            q.pop();
            vis[now] = false;
            for (int i = last[now]; i; i = edge[i].pre) {
                int to = edge[i].to;
                if (edge[i ^ 1].flow > 0 && dis[now] < dis[to] + edge[i].cost){
                    dis[to] = dis[now] - edge[i].cost;
                    if (!vis[to])
                        q.push(to), vis[to] = true;
                }
            }
        }
        return dis[S] != INF;
    }//SPFA

    int DFS(int u, int flow){
        vis[u] = true;
        if (u == T)
            return flow;
        int used = 0;
        for (int i = last[u]; i; i = edge[i].pre) {
            int v = edge[i].to;
            if (!vis[v] && dis[v] == dis[u] - edge[i].cost && edge[i].flow != 0){
                int minFlow = DFS(v, min(edge[i].flow, flow - used));
                if (minFlow != 0){
                    ans.minCost += (minFlow * edge[i].cost);
                    used += minFlow;
                    edge[i].flow -= minFlow;
                    edge[i ^ 1].flow += minFlow;
                }
                if (flow == used)
                    break;
            }
        }
        return used;
    }//DFS

public:
    Dinic():len(1){}
    void add(int from, int to, int flow, int cost){
        edge[++len] = {to, last[from], flow, cost};
        last[from] = len;
        edge[++len] = {from, last[to], 0, -cost};
        last[to] = len;
    }
    Data main(int S, int T){
        this->S = S;
        this->T = T;
        ans = {};
        while (SPFA()){
            vis[T] = true;
            while (vis[T]){
                memset(vis, false, sizeof(vis));
                ans.maxFlow += DFS(S, INF);
            }
        }
        //cout << "Maximum Flow: " << ans.maxFlow << endl;
        //cout << "Minimum Cost: " << ans.minCost << endl;
        cout << setiosflags(ios::fixed) << setprecision(2) << 1.0 * ans.minCost / ans.maxFlow << endl;
        return ans;
    }
};

int t[65][15];
Dinic dinic;
int main()
{
    int n, m, S = 0, T = 0;
    cin >> m >> n;
    T = n + n * m + 1;
    for (int i = 1; i <= n; ++i) {
        dinic.add(S, i, 1, 0);
    }
    for (int j = 1; j <= m; ++j) {
        for (int k = 1; k <= n; ++k) {
            dinic.add(j * n + k, T, 1, 0);
        }
    }
    int t;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            cin >> t;
            for (int k = 1; k <= n; ++k) {
                dinic.add(i, j * n + k, 1,  k * t);
            }
        }
    }
    dinic.main(S, T);
    return 0;
}

