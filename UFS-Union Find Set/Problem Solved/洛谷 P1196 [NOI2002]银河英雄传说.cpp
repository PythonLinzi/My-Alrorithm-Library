#include <iostream>
using namespace std;

const int N = 30001;
int T, x, y, pre[N], d[N], num[N];
char ch;
//d：距离头节点的距离，num[i]：节点i所属集合元素个数

int find(int x)
{
    if (pre[x] == x)
        return x;
    int tmp = pre[x];
    pre[x] = find(pre[x]); //递归压缩路径
    d[x] += d[tmp];
    num[x] = num[pre[x]];
    return pre[x];
}


int main()
{
    ios_base::sync_with_stdio(false);
    cin >> T;
    for (int i = 0; i < N; ++i) {
        pre[i] = i;
        d[i] = 0;
        num[i] = 1;
    }
    for (int i = 0; i < T; ++i) {
        cin >> ch >> x >> y;
        int fx = find(x), fy = find(y);
        if (ch == 'M'){
            pre[fx] = fy;
            d[fx] += num[fy];
            num[fx] += num[fy];
            num[fy] = num[fx];
        }
        else if (ch == 'C'){
            if (fx == fy)
                cout << abs(d[x] - d[y]) - 1 << endl;
            else
                cout << -1 << endl;
        }
    }
}