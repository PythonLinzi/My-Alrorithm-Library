#include <iostream>
#include <stack>
#include <vector>
#include <cstring>
#include <algorithm>
using namespace std;

const int N = 10005, M = 50005;
int n, m, a, b, label = 0, cnt = 0;
vector<int> g[N];
stack<int> s;
int dfn[N], low[N], out[N], belong[N], have[N], tmp[N];
bool instack[N];


void tarjan(int u)
{
    dfn[u] = low[u] = ++cnt;
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
    int now;
    if (dfn[u] == low[u]){
        label++;
        int cnt_ = 0;
        do{
            now = s.top();
            s.pop();
            instack[now] = false;
            tmp[++cnt_] = now;
            belong[now] = label;
        }while (now != u);
        have[label] = cnt_;
        for (int i = 1; i <= cnt_; ++i) {
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
    for (int i = 0; i < m; ++i) {
        cin >> a >> b;
        g[a].push_back(b);
    }//enter data
    for (int i = 1; i <= n; ++i) {
        if (!dfn[i])
            tarjan(i);
    }
    int ans = 0;
    for (int i = 1; i <= label; ++i) {
        if (out[i] == 0){
            if (ans){
                ans = 0;
                break;
            }
            else{
                ans = have[i];
            }
        }
    }
    cout << ans << endl;
    return 0;
}
