#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

const int N = 10005;
int n, m, x, y, dfn[N], low[N], label = 0, number = 0, num[N], belong[N], tmp[N], out[N];
vector<int> g[N];
stack<int> s;
bool instack[N];


void tarjan(int u)
{
    dfn[u] = low[u] = ++number;
    s.push(u);
    instack[u] = true;
    for (int i = 0; i < g[u].size(); ++i) {
        int v = g[u][i];
        if (!dfn[v]){
            tarjan(v);
            low[u] = min(low[u], low[v]);
        }
        else if (instack[v])
            low[u] = min(low[u], dfn[v]);
    }
    if (dfn[u] == low[u]){
        label++;
        int now, cnt = 0;
        do{
            now = s.top();
            s.pop();
            instack[now] = false;
            tmp[++cnt] = now;
            belong[now] = label;
        }while (now != u);
        num[label] = cnt;
        for (int i = 1; i <= cnt; ++i) {
            int v = tmp[i];
            for (int j = 0; j < g[v].size(); ++j) {
                if (belong[g[v][j]] != label)
                    out[label]++;
            }
        }
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin >> n >> m;
    for (int i = 1; i <= n; ++i)
        dfn[i] = low[i] = 0;
    for (int i = 0; i < m; ++i) {
        cin >> x >> y;
        g[x].push_back(y);
    }//create graph
    for (int i = 1; i <= n; ++i) {
        if (!dfn[i])
            tarjan(i);
    }
    int ans = 0;
    for (int i = 1; i <= label; ++i) {
        if (out[i] == 0 && num[i] > 1)
            ans++;
    }
    cout << ans << endl;
    return 0;
}