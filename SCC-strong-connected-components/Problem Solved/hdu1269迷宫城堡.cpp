#include <iostream>
#include <vector>
#include <stack>
#include <cstring>
#include <algorithm>
using namespace std;

const int N = 10005;
int n, m, a, b, label = 0, number = 0;
vector<int> g[N];
stack<int> s;
int dfn[N], low[N];
bool instack[N];


void init(int n)
{
    label = 0, number = 0;
    memset(dfn, 0, sizeof(dfn));
    memset(low, 0, sizeof(low));
    memset(instack, false, sizeof(instack));
    for (int i = 0; i <= n; ++i) {
        g[i].clear();
    }
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
        do{
            now = s.top();
            s.pop();
            instack[now] = false;
        }while (now != u);
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
        if (label == 1){
            cout << "Yes" << endl;
        }
        else{
            cout << "No" << endl;
        }
    }//while cin
    return 0;
}