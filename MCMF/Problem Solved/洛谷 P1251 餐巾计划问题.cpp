#include <iostream>
#include <cstring>
#include <algorithm>
#include <queue>
#include <vector>
#define maxn 1000005
using namespace std;
typedef long long ll;
const ll inf = 2147483647;

class Dinic
{
    struct Edge{ll to, pre, flow, cost;};
    struct Data{ll maxFlow, minCost;};
    Edge edge[maxn];
    Data ans;
    ll dis[maxn], len = 1, last[maxn], S, T, INF = 4557430888798830399;
    bool vis[maxn];

    bool SPFA(){
        memset(vis, false, sizeof(vis));
        memset(dis, 63, sizeof(dis));
        queue<ll> q;
        q.push(T);
        dis[T] = 0, vis[T] = 1;
        while (!q.empty()){
            ll now = q.front();
            q.pop();
            vis[now] = false;
            for (ll i = last[now]; i; i = edge[i].pre) {
                ll to = edge[i].to;
                if (edge[i ^ 1].flow > 0 && dis[now] < dis[to] + edge[i].cost){
                    dis[to] = dis[now] - edge[i].cost;
                    if (!vis[to])
                        q.push(to), vis[to] = true;
                }
            }
        }
        return dis[S] != INF;
    }//SPFA

    ll DFS(ll u, ll flow){
        vis[u] = true;
        if (u == T)
            return flow;
        ll used = 0;
        for (ll i = last[u]; i; i = edge[i].pre) {
            ll v = edge[i].to;
            if (!vis[v] && dis[v] == dis[u] - edge[i].cost && edge[i].flow != 0){
                ll minFlow = DFS(v, min(edge[i].flow, flow - used));
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
    void add(ll from, ll to, ll flow, ll cost){
        edge[++len] = {to, last[from], flow, cost};
        last[from] = len;
        edge[++len] = {from, last[to], 0, -cost};
        last[to] = len;
    }
    Data main(ll S, ll T){
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
        cout << ans.minCost << endl;
        return ans;
    }
};


Dinic dinic;
int main()  //***** i 代表第i天晚上，i + N 代表第i天早上
{
    ll N, r, p, m, f, n, s;
    cin >> N;
    ll S = 0, T = 2 * N + 1;
    for (ll i = 1; i <= N; ++i) {
        cin >> r;
        dinic.add(S, i, r, 0);
        dinic.add(i + N, T, r, 0);
    }
    cin >> p >> m >> f >> n >> s;
    for (ll i = 1; i <= N; ++i) {
        dinic.add(S, i + N, inf, p);
        if (i + 1 <= N) //延期送洗
            dinic.add(i, i + 1, inf, 0);
        if (i + m <= N) //第i天晚上送到快洗部，第i+m天早上送到
            dinic.add(i, i + N + m, inf, f);
        if (i + n <= N) //第i天晚上送到慢洗部，第i+m天早上送到
            dinic.add(i, i + N + n, inf, s);
    }
    dinic.main(S, T);
    return 0;
}



