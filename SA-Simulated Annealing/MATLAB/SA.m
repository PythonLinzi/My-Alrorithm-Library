% Simulated Annealing Algorithm
clear, clc;
initT = 1000; % 初始温度
finalT = 1; % 结束温度
niter = 1000; % 迭代次数
coef = 0.95; % 衰减系数 attenuation coefficient
K = 1; % 接受准则中的衡量参数
step = 1; % 最大步长
bnds = [-10 10]; % 取值范围
nowT = initT;
nowX = rand(1);
bestX = nowX; % 记录降温全过程的最优值
while nowT > finalT
    for i = 1:niter
        nowY = func(nowX);
        newX = nowX + step * (2 * rand - 1);
        if newX > bnds(1) && newX < bnds(2) % 检查取值范围
            newY = func(newX);
            df = newY - nowY;
            if df < 0
                nowX = newX;
                bestX = nowX;
            elseif exp(-df / (K * nowT)) > rand
                nowX = newX;
            end
        end
    end
    nowT = nowT * coef;
end
% 打印结果
fprintf('best x = %f, min f(x) = %f\n', bestX, func(bestX));
