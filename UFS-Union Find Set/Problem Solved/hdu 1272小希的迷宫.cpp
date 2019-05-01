//题意不明确，鬼屎题目，试错好久
#include <iostream>
#include <algorithm>
using namespace std;
const int N = 100005;
int x, y, pre[N], v[N], cnt = 0, rank_[N];
bool flag = true;


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
    }
    return root;
}


void merge(int x, int y)
{
    int fx = find(x), fy = find(y);
    if (fx != fy){
        if (rank_[fx] > rank_[fy]){
            pre[fy] = fx;
            rank_[fx]++;
        }
        else{
            pre[fx] = fy;
            rank_[fy]++;
        }
    }
    else
        flag = false;
}


int main()
{
    ios_base::sync_with_stdio(false);
    int m = 1;
    for (int i = 0; i < N; ++i) {
        pre[i] = i;
        v[i] = false;
    }//init
    while (cin >> x >> y){
        if (x == -1 || y == -1) break;
        if (x == 0 && y == 0){
            for (int i = 1; i <= m; ++i) {//判断连通性
                if (pre[i] == i && v[i])
                    cnt++;
            }
            if (cnt > 1)
                flag = false;
            if (flag)
                cout << "Yes" << endl;
            else
                cout << "No" << endl;
            for (int i = 1; i < N; ++i) {
                pre[i] = i;
                v[i] = false;
            }
            cnt = 0;
            flag = true;
        }
        else {
            m = max(m, max(x, y));
            v[x] = v[y] = true;
            merge(x, y);
        }
    }
    return 0;
}