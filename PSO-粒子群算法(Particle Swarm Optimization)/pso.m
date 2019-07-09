close all; clear; clc; 
%% Init Population
f= @(x)x .* sin(x) .* cos(2 * x) - 2 * x .* sin(3 * x); % 函数表达式
n = 1; N = 50;                  % 空间维数，种群个体个数
niter = 100;                    % 迭代次数       
bnds = [0 20];                  % 取值范围  
vmin = -1; vmax = 1;            % 最小/大速度限
w = 0.8;                        % 惯性因子
c1 = 2; c2 = 2.1;               % 自我&群体学习因子
c = c1 + c2;
% K:收敛因子(保证收敛性, 通常令c1+c2=4.1, s.t. K=0.729)
K = 2 / (abs(2 - c - sqrt(c * c - 4 * c)));
% x: 个体初始取值
x = bnds(1) * ones(N, n) + (bnds(2) - bnds(1)) * rand(N, n);
y = f(x);
v = rand(N, n);                 % 初始种群的速度  
pbest_x = x;                    % 记录个体历史最优取值
pbest_y = y;                    % 记录个体历史最优值/适应度
gbest_y = min(y);               % 记录种群历史最优值/适应度
gbest_x = x(y == gbest_y);      % 记录种群历史最优取值
x0 = x; y0 = y;                 % 初始值备份
%% Main Loop
for l = 1:niter
   for i = 1:N
      v(i) =  K * (v(i) + c1 * rand() * (pbest_x(i) - x(i)) + c2 * rand() * (gbest_x - x(i)));
      v(i) = min(v(i), vmax); v(i) = max(v(i), vmin);
      x(i) = x(i) + v(i);       % 更新坐标
      y(i) = f(x(i));           % 更新取值/适应度
      if y(i) < pbest_y(i)      % 更新个体最优记录
          pbest_x(i) = x(i);
          pbest_y(i) = y(i);
      end
      if y(i) < gbest_y         % 更新群体最优记录
          gbest_x = x(i);
          gbest_y = y(i);
      end
   end
end
fprintf('Global Minimum: xmin = %f\n', gbest_x);
fprintf('f(xmin) = %f\n', gbest_y);
%% Plot
figure(1);
ezplot(f, [0, 0.01, 20]);
hold on;
scatter(x0, y0, 30, 'go', 'filled');
title('Initial Condition');
figure(2);
ezplot(f, [0 ,0.01, 20]);
hold on;
scatter(gbest_x, gbest_y, 100, 'ro', 'filled');
title('Final Result');
