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


struct Points{
    double x[3] = {getRand(), getRand(), getRand()};
    int size = 3;
};

void print(Points x){
    for (int i = 0; i < x.size; ++i)
        cout << x.x[i] << (i == x.size - 1?"\n":" ");
    return;
}

double target_func(Points p){return p.x[0] * p.x[0] + p.x[1] * p.x[1] + p.x[2] * p.x[2] + 8;}

// 若无约束则可省略惩罚步骤
double f(Points p){ // 违背约束条件则惩罚
    double y = target_func(p), penalty = 0x3f3f3f3f, bnds;
    if (-p.x[0] > 0){y += (penalty * (-p.x[0]));} // -x1 <= 0
    if (-p.x[1] > 0){y += (penalty * (-p.x[1]));} // -x2 <= 0
    if (-p.x[2] > 0){y += (penalty * (-p.x[2]));} // -x3 <= 0
    bnds = -p.x[0] * p.x[0] + p.x[1] - p.x[2] * p.x[2]; // -x1^2 + x2 - x3^2 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = p.x[0] + p.x[1] * p.x[1] + p.x[2] * p.x[2] - 20; // x1 + x2^2 + x3^2 - 20 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = -p.x[0] - p.x[1] * p.x[1] + 2; // -x1 - x2^2 + 2 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = -p.x[1] - 2 * p.x[2] * p.x[2] + 3; // -x2 - 2 * x3^2 + 3 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    return y;
}


const int N = 50, niter = 500;
double vmin = -1, vmax = 1;
double w = 1, c1 = 2, c2 = 2.1;
double c = c1 + c2;
double K = 2 / (abs(2 - c - sqrt(c * c - 4 * c)));
Points x[N], v[N], pbest_x[N], gbest_x, vi;
double y[N], pbest_y[N], gbest_y;
void PSO(){
    // init
    for (int i = 0; i < N; ++i) {y[i] = pbest_y[i] = f(x[i]);}
    gbest_x = x[0]; gbest_y = y[0];
    for (int i = 0; i < N; ++i) {
        if (y[i] < gbest_y){
            gbest_y = y[i];
            gbest_x = x[i];
        }
    }
    // main loop
    for (int l = 0; l < niter; ++l) {
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < vi.size; ++j) {
                vi.x[j] = K * (v[i].x[j] + c1 * getRand()
                        * (pbest_x[i].x[j] - x[i].x[j]) + c2 * getRand() * (gbest_x.x[j] - x[i].x[j]));
                vi.x[j] = min(vi.x[j], vmax);
                vi.x[j] = max(vi.x[j], vmin);
            }
            for (int j = 0; j < x[i].size; ++j) {
                x[i].x[j] += vi.x[j];
            }
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
    cout << "Global Minimum: xmin = ";
    print(gbest_x);
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
 * Global Minimum: xmin = 0.615724 1.1783 0.964955
 * f(xmin) = 10.6986
 * Running Time: 0s
 */
