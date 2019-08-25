#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iomanip>
using namespace std;

/*
 * SA: Simulated Annealing Algorithm
 * 最好多运行几次取最优
 * Parameters:
 * nowT: 初始温度, finalT: 结束温度
 * niter: 迭代次数, coef: 衰减系数-attenuation coefficient
 * K: 衡量参数, step: 最大步长
 * bnds: 取值范围, 注意初始值X0要在X的取值范围内
 * 采用罚函数法将约束条件加入目标函数
 */

double getRand(){ return rand() / double(RAND_MAX);}


struct Points{
    double x1 = getRand(), x2 = getRand(), x3 = getRand();
};


double target_func(Points p){return p.x1 * p.x1 + p.x2 * p.x2 + p.x3 * p.x3 + 8;}

// 若无约束则可省略惩罚步骤
double f(Points p){ // 违背约束条件则惩罚
    double y = target_func(p), penalty = LONG_LONG_MAX, bnds;
    if (-p.x1 > 0){y += (penalty * (-p.x1));} // -x1 <= 0
    if (-p.x2 > 0){y += (penalty * (-p.x2));} // -x2 <= 0
    if (-p.x3 > 0){y += (penalty * (-p.x3));} // -x3 <= 0
    bnds = -p.x1 * p.x1 + p.x2 - p.x3 * p.x3; // -x1^2 + x2 - x3^2 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = p.x1 + p.x2 * p.x2 + p.x3 * p.x3 - 20; // x1 + x2^2 + x3^2 - 20 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = -p.x1 - p.x2 * p.x2 + 2; // -x1 - x2^2 + 2 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    bnds = -p.x2 - 2 * p.x3 * p.x3 + 3; // -x2 - 2 * x3^2 + 3 <= 0
    if (bnds > 0){y += (penalty * bnds);}
    return y;
}


double nowT = 1000, finalT = 1, niter = 10000, coef = 0.99;
double K = 1, step = 1;
int n = 3;
Points x, newx, ansX;
double y = f(x), ansY = f(ansX);


void getNewPoint(){
    newx.x1 = x.x1 + step * (2 * getRand() - 1);
    newx.x2 = x.x2 + step * (2 * getRand() - 1);
    newx.x3 = x.x3 + step * (2 * getRand() - 1);
    return ;
}


void SA(){
    double newy, df1, df2;
    while(nowT > finalT){
        for (int i = 0; i < niter; ++i) {
            y = f(x);
            ansY = f(ansX);
            getNewPoint() ;
            newy = f(newx);
            df1 = newy - y;
            df2 = newy - ansY;
            if (df1 < 0)
                x = newx;
            else if (exp(-df1 / (K * step)) > getRand())
                x = newx;
            if (df2 < 0)
                ansX = newx;
        }
        nowT *= coef;
    }
    cout << setiosflags(ios::fixed)<< setprecision(4);
    cout << "Best X = [" << ansX.x1 << ", " << ansX.x2 << ", "<< ansX.x3;
    cout << "], min f(x) = " << f(ansX) <<endl;
    return ;
}


int main()
{
    ios_base::sync_with_stdio(false);
    time_t s, e;
    srand((unsigned int)time(0));
    time(&s);
    SA();
    time(&e);
    cout << "Running Time: " << e - s << "s" << endl;
    return 0;
}

/*
 * coef = 0.99
 * Best X = [0.5765, 1.1949, 0.9538], min f(x) = 10.6697
 * Running Time: 5s
 */
