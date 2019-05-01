#include <iostream>
using namespace std;

const int N = 30001;
int n, m, k, pre[N], rank_[N], num[N];


int find(int x)
{
    int root = x;
    while (pre[root] != root)
        root = pre[root];
    int now = x, nxt;
    num[x] = num[root];
    while (now != root){
        num[now] = num[root];
        nxt = pre[now];
        pre[now] = root;
        now = nxt;
    }//压缩路径
    return root;
}


void merge(int x, int y)
{
    int fx = find(x), fy = find(y);
    if (fx == fy) // 同一个根节点不需要合并
        return ;
    if (rank_[fx] < rank_[fy]){
        pre[fx] = fy;
        rank_[fy]++;
        num[fy] += num[fx];
    }
    else{
        pre[fy] = fx;
        rank_[fx]++;
        num[fx] += num[fy];
    }
}


int main()
{
    ios_base::sync_with_stdio(false);
    while((cin >> n >> m) && n){
        for (int i = 0; i < n; ++i) {
            pre[i] = i;
            rank_[i] = 0;
            num[i] = 1;
        }//init
        for (int j = 0; j < m; ++j) {
            int x, y;
            cin >> k >> x;
            for (int i = 0; i < k - 1; ++i) {
                cin >> y;
                merge(x, y);
                x = y;
            }
        }
        int root = find(0);
        cout << num[root] << endl;
    }
    return 0;
}