#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
const int maxN = 1000, maxM = 100005;


class Kruskal{
private:
    struct edge{int u, v, w;};
    int pre[maxN], rank[maxN], n, cnt, ans;
    edge e[maxM];
    vector<edge> path;

    static bool cmp(edge x, edge y) {return x.w < y.w;}

    int find(int x)
    {
        int root = x;
        while (root != pre[root])
            root = pre[root];
        int now = x, nxt;
        while (now != root){
            nxt = pre[now];
            pre[now] = root;
            now = nxt;
        }//compress path
        return root;
    }//Find

    void unite(int x, int y)
    {
        int fx = find(x), fy = find(y);
        if (fx == fy)
            return;
        if (rank[fx] > rank[fy]){
            pre[fy] = fx;
            rank[fx]++;
        }
        else{
            pre[fx] = fy;
            rank[fy]++;
        }
        return;
    }//Union

public:
    Kruskal(int V):n(V), cnt(0), ans(0) {}

    void add(int u, int v, int w)
    {
        cnt++;
        e[cnt].u = u;
        e[cnt].v = v;
        e[cnt].w = w;
    }

    void show_ans()
    {
        if (ans == -1){
            cout << "The graph is not connected!" << endl;
            return;
        }
        for (int i = 0; i < path.size(); ++i) {
            cout << path[i].u << " <--> " << path[i].v << " {weight: " << path[i].w << " }" << endl;
        }
        cout << "Minimum Cost: " << ans << endl;
    }

    void calc()
    {
        for (int i = 0; i <= n; ++i) {
            pre[i] = i;
            rank[i] = 0;
        }//init
        sort(e + 1, e + cnt + 1, cmp);
        int k = 0;
        for (int i = 1; i <= cnt; ++i) {
            if (find(e[i].u) != find(e[i].v)){
                ans += e[i].w;
                path.push_back(e[i]);
                k++;
                unite(e[i].u, e[i].v);
            }
            if (k == n - 1)
                break;
        }
        if (k < n - 1)
            ans = -1;
        show_ans();
        return;
    }
};


int main()
{
    ios_base::sync_with_stdio(false);
    int n, m, u, v, w;
    cin >> n >> m;
    Kruskal kruskal(n);
    for (int i = 0; i < m; ++i) {
        cin >> u >> v >> w;
        kruskal.add(u, v, w);
    }
    kruskal.calc();
    return 0;
}

/* test data
6 12
1 2 3
1 3 2
2 3 2
2 4 4
3 5 9
3 4 9
4 5 9
1 5 8
2 6 4
3 6 4
4 6 6
5 6 7

//result
1 <--> 3 {weight: 2 }
2 <--> 3 {weight: 2 }
2 <--> 4 {weight: 4 }
2 <--> 6 {weight: 4 }
5 <--> 6 {weight: 7 }
Minimum Cost: 19
*/

/*
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


void print_edges_ans(vector<edge> ans)
{
    for (int i = 0; i < ans.size(); ++i)
        cout << ans[i].u << "--" << ans[i].v << " {weight: " << ans[i].weight << "}" << endl;
    cout << "Minimum weight cost : " << sum << endl;
}


bool cmp(edge x, edge y) {return x.weight < y.weight;}


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
    if (rx == ry)
        return;
    if (rank_[rx] > rank_[ry]) {
        pre[ry] = rx;
        rank_[rx]++;
    }
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
    return 0;
}
*/
