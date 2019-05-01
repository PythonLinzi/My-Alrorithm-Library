#include <iostream>
#include <cstring>
#include <vector>
#include <stack>
#include <algorithm>
using namespace std;

const int N = 10005, M = 50005;
int dfn[N], low[N], belong[N], n, m, a, b, label = 0, cnt = 0, number = 0, now;
vector<int> g[N];
bool instack[N];
vector< vector<int> > category;
int out[N];
stack<int> s;


void tarjan(int u)
{
    dfn[u] = low[u] = ++label;
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
    }//for
    if (dfn[u] == low[u]){
        number++;
        cnt = 0;
        vector<int> tmp;
        do{
            now = s.top();
            s.pop();
            instack[now] = false;
            belong[now] = number;
            ++cnt;
            tmp.push_back(now);
        }while (now != u);
        category.push_back(tmp);
        for (int i = 0; i < cnt; ++i) {
            int v = tmp[i];
            for (int j = 0; j < g[v].size(); ++j) {
                if (belong[g[v][j]] != number)
                    out[number]++;
            }
        }//for search outdegree
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin>>n>>m;
    for (int i = 0; i < m; ++i) {
        cin>>a>>b;
        g[a].push_back(b);
    }//enter data
    for (int j = 1; j <= n; ++j) {
        if (!dfn[j])
            tarjan(j);
    }
    int ans = -1;
    for (int k = 1; k <= number ; ++k) {
        if (out[k] == 0) {
            if (ans > 0){
                ans = 0;
                break;
            }
            else
                ans = category[k - 1].size();
        }
    }
    cout<<ans<<endl;
    return 0;
}
