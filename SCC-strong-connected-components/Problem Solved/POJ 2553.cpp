#include <iostream>
#include <vector>
#include <stack>
#include <cstring>
#include <algorithm>
using namespace std;

const int N = 5005;
int n, m, a, b, label = 0, number = 0;
vector<int> g[N];
stack<int> s;
int dfn[N], low[N], belong[N], out[N];
bool instack[N];
vector<int> ans;


void init(int n)
{
    label = 0, number = 0;
    memset(dfn, 0, sizeof(dfn));
    memset(low, 0, sizeof(low));
    memset(instack, false, sizeof(instack));
    for (int i = 0; i <= n; ++i) {
        g[i].clear();
    }
    memset(out, 0, sizeof(out));
    ans.clear();
}


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
    int now;
    if (dfn[u] == low[u]){
        label++;
        vector<int> tmp;
        do{
            now = s.top();
            s.pop();
            instack[now] = false;
            tmp.push_back(now);
            belong[now] = label;
        }while (now != u);
        for (int i = 0; i < tmp.size(); ++i) {
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
    while ((cin >> n) && n){
        cin >> m;
        init(n);
        for (int i = 0; i < m; ++i) {
            cin >> a >> b;
            g[a].push_back(b);
        }//enter data
        for (int i = 1; i <= n; ++i) {
            if (!dfn[i])
                tarjan(i);
        }
        for (int i = 1; i <= n; ++i) {
            if (out[belong[i]] == 0)
                ans.push_back(i);
        }
        for (int i = 0; i < ans.size(); ++i) {
            cout << ans[i] << (i == ans.size() - 1?"\n":" ");
        }
        if (ans.empty())
            cout << endl;
    }//while cin
    return 0;
}