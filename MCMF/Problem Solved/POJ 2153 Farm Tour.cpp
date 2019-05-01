#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
#include <vector>
#define maxn 100005
using namespace std;
const int INF = 0X3f3f3f3f;

/*
 * S --(2,0)--> 1 .... N --(2,0)--> T
 * 转化为求最大流为2的最小费用流
 */


class Dinic
{
    struct Edge{int to, pre, flow, cost;};
    struct Data{int maxFlow, minCost;};
    Edge edge[maxn];
    Data ans;
    int dis[maxn], len, last[maxn], S, T;
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
        len++;
        edge[len].to = to;
        edge[len].pre = last[from];
        edge[len].flow = flow;
        edge[len].cost = cost;
        last[from] = len;
        len++;
        edge[len].to = from;
        edge[len].pre = last[to];
        edge[len].flow = 0;
        edge[len].cost = -cost;
        last[to] = len;
    }
    Data main(int S, int T){
        this->S = S;
        this->T = T;
        while (SPFA()){
            vis[T] = true;
            while (vis[T]){
                memset(vis, false, sizeof(vis));
                ans.maxFlow += DFS(S, INF);
            }
        }
        cout << ans.minCost << endl;
        return ans;
    }
};


Dinic dinic;
int main()
{
    int n, m, from, to, cost;
    cin >> n >> m;
    for (int i = 0; i < m; ++i) {
        cin >> from >> to >> cost;
        dinic.add(from, to, 1, cost);
        dinic.add(to, from, 1, cost);
    }
    int S = 0, T = n + 1;
    dinic.add(S, 1, 2, 0);
    dinic.add(n, T, 2, 0);
    dinic.main(S, T);
    return 0;
}

