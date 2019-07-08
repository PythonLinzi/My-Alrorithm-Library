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
 * bnds: 取值范围
 */

double getRand(){ return rand() / double(RAND_MAX);}


struct Points{
    double x1 = getRand(), x2 = getRand(), x3 = getRand();
};


double func(Points p){return p.x1 * p.x1 + p.x2 * p.x2 + p.x3 * p.x3 + 8;}


double nowT = 1000, finalT = 1, niter = 10000, coef = 0.999;
double K = 1, step = 1;
int n = 3;
Points x, newx, ansX;
double y = func(x);

bool in_bnds(Points p){
    if (!(p.x1>0 && p.x2>0 && p.x3>0))
        return false;
    if (p.x1 * p.x1 - p.x2 + p.x3 * p.x3 >= 0){
        if (-p.x1 - p.x2 * p.x2 - p.x3 * p.x3 + 20 >= 0){
            if (p.x1 + p.x2 * p.x2 - 2 >= 0){
                if (p.x2 + 2 * p.x3 * p.x3 - 3 >= 0){
                    return true;
                }
            }
        }
    }
    return false;
}


void getNewPoint(){
    newx.x1 += step * (2 * getRand() - 1);
    newx.x2 += step * (2 * getRand() - 1);
    newx.x3 += step * (2 * getRand() - 1);
    return ;
}

void SA(){
    double newy, df;
    while(nowT > finalT){
        for (int i = 0; i < niter; ++i) {
            y = func(x);
            getNewPoint() ;
            if(in_bnds(newx)){
                newy = func(newx);
                df = newy - y;
                if(df < 0)
                    ansX = x = newx;
                else if(exp(-df / (K * nowT)) > getRand())
                    x = newx;
            }
        }
        nowT *= coef;
    }
    cout << setiosflags(ios::fixed)<< setprecision(4);
    cout << "Best X = [" << ansX.x1 << ", " << ansX.x2 << ", "<< ansX.x3;
    cout << "], min f(x) = " << func(ansX);
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
 * coef = 0.999
 * Best X = [0.3503, 0.8960, 0.8228], min f(x) = 9.6025
 * Running Time: 5s
 */
