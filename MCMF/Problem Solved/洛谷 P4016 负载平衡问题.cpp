#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
#include <vector>
#define maxn 10005
using namespace std;
const int INF = 0X3f3f3f3f;

/*
 * 转化为最小费用最大流问题
 * 最大流：需要转移的大于平均值的货物数量
 * 多于平均值的部分相当于S给的，少于平均值的部分相当于给T
 * 最小费用：货物最小移动次数
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
        edge[++len] = {to, last[from], flow, cost};
        last[from] = len;
        edge[++len] = {from, last[to], 0, -cost};
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

int a[105];
Dinic dinic;
int main()
{
    ios_base::sync_with_stdio(false);
    int n, sum = 0;
    cin >> n;
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
        sum += a[i];
    }
    int S = 0, T = n + 1;
    int ave = sum / n;
    for (int i = 1; i <= n; ++i) {
        if (a[i] - ave > 0){
            dinic.add(S, i, a[i] - ave, 0);
        }
        else{
            dinic.add(i, T, ave - a[i], 0);
        }
    }
    for (int i = 1; i <= n; ++i) {
        if (i != 1)
            dinic.add(i, i - 1, INF, 1);
        if (i != n)
            dinic.add(i, i + 1, INF, 1);
    }
    dinic.add(1, n, INF, 1);
    dinic.add(n, 1, INF, 1);
    dinic.main(S, T);
    return 0;
}
