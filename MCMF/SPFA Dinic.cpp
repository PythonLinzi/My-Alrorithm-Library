#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
#include <vector>
#define maxn 1000005
using namespace std;
//typedef ll long long
const int INF = 0X3f3f3f3f;
//INF = 4557430888798830399; if long long

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
        memset(dis, 0x3f, sizeof(dis));//memset(dis, 63, sizeof(dis));
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
        //有些版本的编译器不行，比如POJ？
        /*
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
        last[to] = len;*/
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
        cout << "Maximum Flow: " << ans.maxFlow << endl;
        cout << "Minimum Cost: " << ans.minCost << endl;
        return ans;
    }
};


Dinic dinic;
int main()
{
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    for (int i = 0; i < m; ++i) {
        int from, to, flow, cost;
        cin >> from >> to >> flow >> cost;
        dinic.add(from, to, flow, cost);
    }//create graph
    dinic.main(s, t);
    return 0;
}

/*
 * test data
6 9 1 6
1 2 8 2
1 4 7 8
2 4 5 5
2 3 9 2
3 4 2 1
4 5 9 3
5 3 6 4
3 6 5 6
5 6 10 7
 */
