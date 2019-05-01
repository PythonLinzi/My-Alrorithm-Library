#include <iostream>
#include <queue>
#include <cstring>
#include <algorithm>
using namespace std;

const int maxn = 205;
int n, m; // n：边数  m：点数
bool vis[maxn];
int g[maxn][maxn], pre[maxn], ans = 0;


void show_ans()
{
    cout << "Maximum flow: " << ans << endl;
}


void Ford_Fulkerson()
{
    while (true){
        memset(vis, false, sizeof(vis)); //重置:恢复未访问
        memset(pre, -1, sizeof(pre));
        queue<int> q;
        int now = 1;
        q.push(now);
        vis[now] = true;
        while (!q.empty()){
            now = q.front();
            q.pop();
            if (now == m) break;//到达汇点停止寻找增广路径---很关键
            for (int i = 1; i <= m; ++i) {
                if (g[now][i] && !vis[i]){ //每次父亲节点都要更新,权值减为0的边就不算了.
                    vis[i] = true;
                    q.push(i);
                    pre[i] = now;
                }
            }
        }//BFS: search augmentation path
        if (!vis[m]) //不存在增广路了:end loop
            break;
        int minp = 0xFFFF;
        for (int u = m; u > 1; u = pre[u]) // 寻找增广路径上的最多增加流量
            minp = min(minp, g[pre[u]][u]);
        for (int u = m; u > 1; u = pre[u]) {
            g[pre[u]][u] -= minp; //前向弧减去
            g[u][pre[u]] += minp; //后向弧加上 //存在圆环,这句话关键
        }
        ans += minp; //当前增广路径增加的流
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin >> n >> m;
    memset(g, 0, sizeof(g));
    int u, v, w;
    for (int i = 1; i <= n; ++i) {
        cin >> u >> v >> w;
        g[u][v] += w;
    }//create graph
    Ford_Fulkerson();
    show_ans();
    return 0;
}