#include <iostream>
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iomanip>
using namespace std;

/*
 * PSO: Particle Swarm Optimization Algorithm
 * 最好多运行几次取最优
 * Parameters:
 *  N: 种群个体数量(一般取20~50 or 100~200), niter: 迭代次数
 *  vmin, vmax: 最大最小速度--限定步长
 *  w: 惯性因子(>=0)
 *  c1, c2: 学习因子(通常c1=c2=2)
 *  K: 收敛因子(保证收敛性, 通常令c1+c2=4.1, s.t. K=0.729)
 *  bnds: 取值范围
 * 采用罚函数法将约束条件加入目标函数
 */

double getRand(){ return rand() / double(RAND_MAX);}


double target_func(double x) {return (x - 2) * (x + 3) * (x + 8) * (x - 9);}

// 若无约束则可省略惩罚步骤
double f(double x){ // 违背约束条件则惩罚
    double y = target_func(x), penalty = 0x3f3f3f3f, bnds;
    bnds = x - 10; // x - 10 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = -x - 10; // -x - 10 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    return y;
}


const int N = 50, niter = 500;
double vmin = -1, vmax = 1;
double w = 1, c1 = 2, c2 = 2.1;
double c = c1 + c2;
double K = 2 / (abs(2 - c - sqrt(c * c - 4 * c)));
double x[N], v[N], pbest_x[N], gbest_x, vi;
double y[N], pbest_y[N], gbest_y;
void PSO(){
    // init
    for (int i = 0; i < N; ++i) {
        x[i] = pbest_x[i] = getRand();
        y[i] = pbest_y[i] = f(x[i]);
        v[i] = getRand();
    }
    gbest_x = x[0];
    gbest_y = y[0];
    for (int i = 0; i < N; ++i) {
        if (y[i] < gbest_y){
            gbest_y = y[i];
            gbest_x = x[i];
        }
    }
    // main loop
    for (int l = 0; l < niter; ++l) {
        for (int i = 0; i < N; ++i) {
            vi = K * (v[i] + c1 * getRand() * (pbest_x[i] - x[i]) + c2 * getRand() * (gbest_x - x[i]));
            vi = min(vi, vmax);
            x[i] += max(vi, vmin);
            y[i] = f(x[i]);
            if (y[i] < pbest_y[i]){
                pbest_x[i] = x[i];
                pbest_y[i] = y[i];
            }
            if (y[i] < gbest_y){
                gbest_x = x[i];
                gbest_y = y[i];
            }
        }
    }
    cout << "Global Minimum: xmin = " << gbest_x << endl;
    cout << "f(xmin) = " << gbest_y << endl;
    return;
}



int main()
{
    ios_base::sync_with_stdio(false);
    time_t s, e;
    srand((unsigned int)time(0));
    time(&s);
    PSO();
    time(&e);
    cout << "Running Time: " << e - s << "s" << endl;
    return 0;
}

/*
 * Global Minimum: xmin = 6.48418
 * f(xmin) = -1549.73
 * Running Time: 0s
 */
