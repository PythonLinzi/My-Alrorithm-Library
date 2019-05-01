#include <iostream>
#include <cstring>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

const int N = 5005, M = 50005;
int n, m, cnt = 0, number = 0, j;
int g[N][N];
int dfn[N], low[N];
bool flag[N];
stack<int> s;
vector<int> ans;
vector< vector<int> > category;

void init()
{
    memset(g, 0, sizeof(g));
    memset(dfn, 0, sizeof(dfn));
    memset(low, 0, sizeof(low));
    memset(flag, false, sizeof(flag));
}


void tarjan(int u)
{
    dfn[u] = low[u] = ++cnt;
    s.push(u);
    flag[u] = true;
    for (int v = 1; v <= n; ++v) {
        if (g[u][v]){
            if (!dfn[v]){
                tarjan(v);
                low[u] = min(low[u], low[v]);
            }
            else if (flag[v])
                low[u] = min(low[u], dfn[v]);
        }
    }
    if (dfn[u] == low[u]){
        number++;
        vector<int> tmp;
        do{
            j = s.top();
            tmp.push_back(j);
            s.pop();
            flag[j] = false;
        }while (j != u);
        category.push_back(tmp);
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    int a, b, c;
    cin>>n>>m;
    for (int i = 0; i < m; ++i) {
        cin>>a>>b>>c;
        if (c == 1)
            g[a][b] = 1;
        else
            g[a][b] = g[b][a] = 1;
    }//enter data
    for (int k = 1; k <= n; ++k) {
        tarjan(k);
        for (int idx = 0; idx < number; ++idx) {
            if (category[idx].size() > ans.size())
                ans = category[idx];
        }
    }
    int l = ans.size();
    sort(ans.begin(), ans.end());
    cout<<l<<endl;
    for (int k = 0; k <l ; ++k) {
        cout<<ans[k]<<(k == l - 1?"\n":" ");
    }
    return 0;
}