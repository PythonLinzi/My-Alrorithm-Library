#include<iostream>
#include<queue>
#include<algorithm>
#include<vector>
#include <cstring>
using namespace std;
const int MAXN = 10005;
const int MAXM = 50005;
const int inf = 0x3f3f3f3f;

struct Node{
    int u,dis;
    bool operator > (const Node &b) const {
        return dis > b.dis;
    }
};

struct Edge{ int to,nxt,w;}e[MAXM << 1];


int head[MAXN], tot, dis[MAXN];
int n, m, S, u, v, w;
priority_queue<Node, vector<Node>, greater<Node>>q;
bool vis[MAXN];


void add_edge(int u,int v,int w) {
    e[++tot].to = v;
    e[tot].w = w;
    e[tot].nxt = head[u];
    head[u] = tot;
    return;
}


void dijkstra()
{
    memset(dis, inf, sizeof(dis));
    memset(vis,0,sizeof vis );
    Node Now;
    q.push((Node){S,0});
    dis[S] = 0;
    while(!q.empty()) {
        Now = q.top();
        q.pop();
        if(vis[Now.u]) {
            continue;
        }
        int u = Now.u;
        vis[u] = 1;
        for(int i=head[u]; i; i=e[i].nxt) {
            int v = e[i].to;
            if(dis[v] > dis[u] + e[i].w) {
                dis[v] = dis[u] + e[i].w;
                q.push((Node){v,dis[v]});
            }
        }
    }
    for(int i=1; i<=n; ++i){
        printf("%d ", dis[i]);
    }
    return;
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin >> n >> m >> S;
    for(int i=1; i<=m; ++i) {
        cin >> u >> v >> w;
        add_edge(u, v, w);
    }
    dijkstra();
    return 0;
}

/*
 * Input
5 7 1
1 2 10
1 4 30
1 5 100
2 3 50
3 5 10
4 3 20
4 5 60
 * Output
0 10 50 30 60
 */
