#include <iostream>
using namespace std;

const int N = 50005;
int n, m, a, b, cnt = 0, pre[N], rank_[N];


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


int main()
{
    ios_base::sync_with_stdio(false);
    while ((cin >> n >> m) && n){
        cnt++;
        for (int i = 1; i <= n; ++i) {
            pre[i] = i;
            rank_[i] = 0;
        }
        for (int i = 0; i < m; ++i) {
            cin >> a >> b;
            merge(a, b);
        }
        int ans = 0;
        for (int i = 1; i <= n; ++i) {
            if (pre[i] == i)
                ans++;
        }
        cout << "Case " << cnt << ": " << ans << endl;
    }
    return 0;
}