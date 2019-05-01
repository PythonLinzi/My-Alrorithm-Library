#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;


typedef struct edge{
    int u, v, weight;
}edge;


const int N = 10005;
edge E[N];
int n, m, pre[N], rank_[N], sum = 0;
vector<edge> ans;


void init()
{
    for (int i = 1; i <= n; ++i) {
        pre[i] = i;
        rank_[i] = 0;
    }
    ans.clear();
}


bool cmp(edge x, edge y) {return x.weight < y.weight;}


void print_edges_ans(vector<edge> ans)
{
    for (int i = 0; i < ans.size(); ++i)
        cout << ans[i].u << "--" << ans[i].v << " {weight: " << ans[i].weight << "}" << endl;
    cout << "Minimum weight cost : " << sum << endl;
}


int find(int x)
{
    int root = x;
    while (pre[root] != root)
        root = pre[root];
    int now = x, nxt;
    while (now != root){
        nxt = pre[now];
        pre[now] = root;
        now = nxt;
    }//压缩路径
    return root;
}


void merge(int x, int y)
{
    int rx = find(x), ry = find(y);
    if (rank_[rx] < rank_[ry])
        pre[rx] = ry;
    else if (rank_[rx] > rank_[ry])
        pre[ry] = rx;
    else{
        pre[rx] = ry;
        rank_[ry]++;
    }
}


void kruskal()
{
    init();
    int cnt = 0;
    sort(E + 1, E + m + 1, cmp);
    for (int i = 1; i <= m; ++i) {
        if (find(E[i].u) != find(E[i].v)){
            sum += E[i].weight;
            ans.push_back(E[i]);
            merge(E[i].u, E[i].v);
            cnt++;
        }
        if (cnt == n - 1)
            break;
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin >> n >> m;
    for (int i = 1; i <= m; ++i) {
        cin >> E[i].u >> E[i].v >> E[i].weight;
    }//enter data
    kruskal();
    print_edges_ans(ans);
}