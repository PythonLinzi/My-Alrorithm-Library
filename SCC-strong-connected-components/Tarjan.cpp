#include <iostream>
#include <algorithm>
#include <cstring>
#include <stack>
using namespace std;

const int maxn = 105;
int dfn[maxn], low[maxn];
bool flag[maxn];
int length, cnt = 0, number = 0;
int matrix[105][105]={
        {0,1,1,0,0,0},{0,0,0,1,0,0},{0,0,0,1,1,0},
        {1,0,0,0,0,1},{0,0,0,0,0,1},{0,0,0,0,0,0}
};
stack<int> s;
vector<vector<int>> ans;


vector<vector<int>> tarjan(int u)
{
    dfn[u] = low[u] = ++cnt;
    s.push(u);
    flag[u] = true;
    for (int v = 0; v < length; ++v) {
        if (matrix[u][v]){
            if (!dfn[v]){
                tarjan(v);
                low[u] = min(low[u], low[v]);
            }
            else if(flag[v])
                low[u] = min(low[u], dfn[v]);
        }
    }
    int j;

    if (dfn[u] == low[u]){
        number++;
        vector<int> tmp;
        do {
            j = s.top();
            tmp.push_back(j);
            s.pop();
            flag[j] = false;
        }while (j != u);
        ans.push_back(tmp);
    }
    return ans;
}


void print_ans(vector<vector<int>> ans)
{
    int n = ans.size();
    for (int i = 0; i < n; ++i) {
        int m = ans[i].size();
        for (int j = 0; j < m; ++j) {
            cout<<ans[i][j]<<(j == m-1?"\n":" ");
        }
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    memset(dfn, 0, sizeof(dfn));
    memset(low, 0, sizeof(low));
    memset(flag, false, sizeof(flag));
    length = 6;
    vector<vector<int>> ans = tarjan(0);
    print_ans(ans);
    return 0;
}