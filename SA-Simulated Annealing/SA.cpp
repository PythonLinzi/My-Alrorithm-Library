#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iomanip>
using namespace std;
/*
 * SA: Simulated Annealing Algorithm
 * 最好多运行几次
 * Parameters:
 * nowT: 初始温度, finalT: 结束温度
 * niter: 迭代次数, coef: 衰减系数-attenuation coefficient
 * K: 衡量参数, step: 最大步长
 */

double getRand(){ return rand() / double(RAND_MAX);}

bool in_bnds(double x) {return (x > -10 && x < 10);}

double func(double x) {return (x - 2) * (x + 3) * (x + 8) * (x - 9);}

double nowT = 1000, finalT = 1, niter = 1000, coef = 0.999;
double K = 1, step = 1;
double x = getRand();
double y = func(x), ansX = x;

void SA(){
    double newx, newy, df;
    while(nowT > finalT){
        for (int i = 0; i < niter; ++i) {
            y = func(x);
            newx = x + step * (2 * getRand() - 1);
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
    cout << "Best X = " << ansX << ", min f(x) = " << func(ansX);
    return ;
}


int main()
{
    ios_base::sync_with_stdio(false);
    srand((unsigned int)time(0));
    SA();
    return 0;
}
