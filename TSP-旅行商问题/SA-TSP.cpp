#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <vector>
using namespace std;

const int n = 31;
double x[31] = {1, 3, 6, 12, 19, 22, 23, 20, 21, 22.5, 40, 44, 42, 36, 39, 58, 62, 88, 90, 83, 71, 67, 64, 52, 84, 87, 71, 71, 58, 80, 1};
double y[31] = {99, 50, 64, 40, 41, 42, 37, 54, 60, 60.5, 26, 20, 35, 83, 95, 33, 30.5, 6, 38, 44, 42, 57, 59, 62, 65, 74, 70, 77, 68, 66, 99};
double d[31][31];
int p0[n], p[n];
double dis0 = 0, dis = 0x3f3f3f3f;
vector<int> tmp;

double myrand(){ return rand() / double(RAND_MAX);}


void init(){
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            d[i][j] = sqrt((x[i] - x[j]) * (x[i] - x[j]) + (y[i] - y[j]) * (y[i] - y[j]));
        }
    }
    return;
}


void MonteCarlo(){ // 采用蒙特卡洛算法求一个较好初值
    for(int l = 0; l < n; ++l){tmp.push_back(l);}
    tmp.push_back(0);
    for(int i = 0; i < 1000; ++i){
        random_shuffle(tmp.begin() + 1, tmp.end() - 1);
        for(int j = 0; j < n; ++j){p0[j] = tmp[j];}
        dis0 = 0;
        for(int j = 0; j < n; ++j){
            dis0 += d[p0[j]][p0[j + 1]];
        }
        if(dis0 < dis){
            for(int j = 0; j < n; ++j){p[j] = p0[j];}
            dis = dis0;
        }
    }
    return;
}


void SA(){ // Simulated Annealing
    double T = 1000, finalT = 1, coef = 0.99, df = 0;
    int K = 1, niter = 1000; // 衡量系数, 每轮迭代次数
    int u, v;
    MonteCarlo();
    while(T > finalT){ // 模拟退火过程
        for(int l = 0; l < niter; ++l){
            u = 1 + int((n - 3) * myrand()); // 1 <= u < 30
            v = 1 + int((n - 3) * myrand()); // 1 <= v < 30
            if (u > v){int tt = v; v = u; u = tt;}
            if (u == v){ continue; }
            df = d[p[u - 1]][p[v]] + d[p[u]][p[v + 1]] - d[p[u - 1]][p[u]] - d[p[v]][p[v + 1]];
            if(df < 0){ // 接受新解
                while (u < v) {
                    int t = p[v]; p[v] = p[u]; p[u] = t;
                    u++; v--;
                }
                dis += df;
            }
            else if(exp(-df / K * T) > myrand()){ // 依概率接受新解
                while(u < v){
                    int t = p[v]; p[v] = p[u]; p[u] = t;
                    u++; v--;
                }
                dis += df;
            }
        }
        T *= coef;
    }
    cout << "Path: ";
    for(int i = 0; i < n + 1; ++i){
        cout << p[i] << (i == n?"\n":" ");
    }
    cout << "Minimum Distance = " << dis << endl;
    return;
}


int main()
{
    ios_base::sync_with_stdio(false);
    time_t s, e;
    srand((unsigned int)time(0));
    init();
    time(&s);
    SA();
    time(&e);
    cout << setprecision(2) << setiosflags(ios::fixed) << setprecision(4);
    cout << "Running Time: " << e - s << "s" << endl;
    return 0;
}

/*
 * Path: 0 2 9 8 7 1 3 4 5 6 12 10 11 15 16 20 17 18 19 24 29 25 27 26 21 22 28 23 13 14 30 0
 * Minimum Distance = 433.736
 * Running Time: 0s
 */
