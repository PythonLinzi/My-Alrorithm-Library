#include <iostream>
#include <stack>
#include <vector>
#include <algorithm>
using namespace std;

const int N = 100005, M = 500005;
int n, m, cnt = 0, label = 0, a, b;
int dfn[N], low[N], belong[N], first[N], indegree[N], tmp[N];
bool instack[N];
vector<int> g[N], gt[N];
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
    int j;
    if (dfn[u] == low[u]){
        label++;
        int cnt_ = 0;
        do{
            j = s.top();
            s.pop();
            instack[j] = false;
            belong[j] = label;
            tmp[++cnt_] = j;
        }while (j != u);
        for (int i = 1; i <= cnt_ ; ++i) {
            int v = tmp[i];
            for (int k = 0; k < gt[v].size(); ++k) {
                if (belong[gt[v][k]] != label)
                    indegree[label]++;
            }
        }//for search indegree
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin>>n>>m;
    for (int i = 0; i < m; ++i) {
        cin>>a>>b;
        g[a].push_back(b);
        gt[b].push_back(a);
    }//enter data
    for (int j = 1; j <= n ; ++j) {
        if (!dfn[j]) {
            tarjan(j);
        }
    }
    int ans = label;
    for (int k = 1; k <= label; ++k) {
        if (indegree[k])
            ans--;
    }
    cout<<ans<<endl;
    return 0;
}