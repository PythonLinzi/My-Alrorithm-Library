close all; clear; clc; 
%% Init Population
n = 3; N = 50;                  % 空间维数，种群个体个数
niter = 1000;                   % 迭代次数       
bnds = [0, 100;0, 100;0, 100];  % 取值范围  
vmin = -1; vmax = 1;            % 最小/大速度限
w = 0.8;                        % 惯性因子
c1 = 2; c2 = 2.1;               % 自我&群体学习因子
c = c1 + c2;
% K:收敛因子(保证收敛性, 通常令c1+c2=4.1, s.t. K=0.729)
K = 2 / (abs(2 - c - sqrt(c * c - 4 * c)));
% x: 个体初始取值
x = rand(N, n); y = rand(N, 1);
for i = 1:N
   for j = 1:n
      x(i, j) =  x(i, j) * (bnds(j, 2) - bnds(j, 1)) + bnds(j, 1);
   end
   y(i) = func(x(i,:));
end
v = rand(N, n);                 % 初始种群的速度
pbest_x = x;                    % 记录个体历史最优取值
pbest_y = y;                    % 记录个体历史最优值/适应度
gbest_y = min(y);               % 记录种群历史最优值/适应度
gbest_x = x(y == gbest_y, :);   % 记录种群历史最优取值
x0 = x; y0 = y;                 % 初始值备份
%% Main Loop
for l = 1:niter
   for i = 1:N
      for j = 1:n
          v(i, j) =  K * (v(i, j) + c1 * rand() * (pbest_x(i, j) - x(i, j)) + c2 * rand() * (gbest_x(j) - x(i, j)));
          v(i, j) = min(v(i, j), vmax); v(i, j) = max(v(i, j), vmin);
          x(i, j) = x(i, j) + v(i, j);       % 更新坐标
      end
      y(i) = func(x(i,:));           % 更新取值/适应度
      if y(i) < pbest_y(i)      % 更新个体最优记录
          pbest_x(i,:) = x(i,:);
          pbest_y(i) = y(i);
      end
      if y(i) < gbest_y         % 更新群体最优记录
          gbest_x = x(i,:);
          gbest_y = y(i);
      end
   end
end
fprintf('Global Minimum: xmin = (%f, %f, %f)\n', gbest_x);
fprintf('f(xmin) = %f\n', gbest_y);
