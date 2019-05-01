#include <iostream>
#include <cstring>
#include <stack>
#include <vector>
#include <cstring>
#include <algorithm>
using namespace std;

const int N = 30005;
int n, p, r, label = 0, cnt = 0, a, b;
vector<int> g[N], gt[N];
int dfn[N], low[N], buy[N], belong[N], indegree[N], cost[N], tmp[N];
bool instack[N];
stack<int> s;


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
        int k = 0;
        do{
            now = s.top();
            s.pop();
            instack[now] = false;
            tmp[++k] = now;
            belong[now] = label;
        }while (now != u);
        int tmp_p = 2000005;
        for (int i = 1; i <= k; ++i) {
            int v = tmp[i];
            if (buy[v] != -1)
                tmp_p = min(tmp_p, buy[v]);
            for (int j = 0; j < gt[v].size(); ++j) {
                if (belong[gt[v][j]] != label)
                    indegree[label]++;
            }
        }
        cost[label] = tmp_p;
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    memset(buy, -1, sizeof(buy));
    cin>>n>>p;
    for (int i = 0; i < p; ++i) {
        cin>>a>>b;
        buy[a] = b;
    }//enter data_1
    cin>>r;
    for (int i = 0; i < r; ++i) {
        cin>>a>>b;
        g[a].push_back(b);
        gt[b].push_back(a);
    }//enter data_2
    for (int i = 1; i <= n; ++i) {
        if (!dfn[i] && buy[i] > 0) {
            tarjan(i);
        }
    }
    for (int i = 1; i <=n ; ++i) {
        if (!dfn[i]) {
            cout << "NO" << endl;
            cout << i << endl;
            return 0;
        }
    }
    int sum = 0;
    for (int i = 1; i <= label; ++i) {
        if (indegree[i] == 0){
            sum += cost[i];
        }
    }
    cout << "YES" << endl << sum << endl;
    return 0;
}
