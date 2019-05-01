#include <iostream>
using namespace std;

const int N = 1005;
int T, n, m, a, b, pre[N], rank_[N];


int find(int x)
{
    int root = x;
    while (pre[root] != root)
        root = pre[root];
    int i = x, j;
    while (i != root){
        j = pre[i];
        pre[i] = root;
        i = j;
    }//压缩路径
    return root;
}


void merge(int x, int y)
{
    int rx = find(x), ry = find(y);
    if (rx == ry)
        return ;
    if (rank_[rx] < rank_[ry])
        pre[rx] = ry;
    else if(rank_[ry] < rank_[rx])
        pre[ry] = rx;
    else {
        pre[rx] = ry;
        rank_[ry]++;
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin >> T;
    while (T--){
        cin >> n >> m;
        for (int i = 1; i <= n; ++i) {
            pre[i] = i;
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
        cout << ans << endl;
    }
    return 0;
}