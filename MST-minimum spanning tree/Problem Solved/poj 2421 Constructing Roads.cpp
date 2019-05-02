#include <iostream>
#include <cstring>
#include <algorithm>
using namespace std;

const int maxn = 105;
int n, g[maxn][maxn], Q;

class Kruskal{
private:
    struct edge{int u, v, w;};
    int pre[maxn], rank[maxn], n, cnt, ans;
    edge e[maxn * maxn];

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
    Kruskal(int V):n(V), cnt(0), ans(0)
    {
        for (int i = 0; i <= V; ++i) {
            pre[i] = i;
            rank[i] = 0;
        }//init
        for (int i = 1; i <= V; ++i) {
            for (int j = 1; j <= V; ++j) {
                if (i != j){
                    cnt++;
                    e[cnt].u = i;
                    e[cnt].v = j;
                    e[cnt].w = g[i][j];
                }
            }
        }
    }//Kruskal init

    void calc()
    {
        sort(e + 1, e + cnt + 1, cmp);
        int k = 0;
        for (int i = 1; i <= cnt; ++i) {
            if (find(e[i].u) != find(e[i].v)){
                ans += e[i].w;
                k++;
                unite(e[i].u, e[i].v);
            }
            if (k == n - 1)
                break;
        }
        cout << ans << endl;
        return;
    }
};



int main()
{
    ios_base::sync_with_stdio(false);
    cin >> n;
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            cin >> g[i][j];
        }
    }//create graph
    cin >> Q;
    int x, y;
    for (int i = 0; i < Q; ++i) {
        cin >> x >> y;
        g[x][y] = g[y][x] = 0;
    }//modify graph
    Kruskal kruskal(n);
    kruskal.calc();
    return 0;
}
