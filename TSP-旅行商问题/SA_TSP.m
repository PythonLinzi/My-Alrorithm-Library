clear, clc;
pos_X = [1, 3, 6, 12, 19, 22, 23, 20, 21, 22.5, 40, 44, 42, 36, 39, 58, 62, 88, 90, 83, 71, 67, 64, 52, 84, 87, 71, 71, 58, 80, 1];
pos_Y = [99, 50, 64, 40, 41, 42, 37, 54, 60, 60.5, 26, 20, 35, 83, 95, 33, 30.5, 6, 38, 44, 42, 57, 59, 62, 65, 74, 70, 77, 68, 66, 99];
n = size(pos_X, 2);
d = zeros(n);                                % 初始化距离矩阵d
for i = 1:n                                  % 计算距离Matrix
   for j = 1:n
        d(i,j) = sqrt((pos_X(i) - pos_X(j))^2 + (pos_Y(i) - pos_Y(j))^2);
   end
end
path = [];                                   % 巡航路径
y = inf;                                     % 初始化距离
rand('state', sum(clock));                   % 随机数生成器初始化
for j = 1:1000                               % Monte Carlo求较好的初始解
    path0 = [1 1 + randperm(n - 2), n];
    tmp = 0;
    for i = 1:n-1
        tmp = tmp + d(path0(i), path0(i+1));
    end
    if tmp < y
        path = path0;
        y = tmp;
    end
end
T = 1000;                                    % 初始温度
finalT = 1;                                  % 结束温度
coef = 0.99;                                 % 温度衰减系数
niter = 1000;                                % 每轮迭代次数
K = 1;                                       % 衡量系数
bestPath = []; bestY = inf;
while T > finalT                             % 模拟退火过程
    for i = 1:niter                          % 产生新解
       new = 2 + floor((n-2) * rand(1, 2));  % 产生新解
       new = sort(new); 
       u = new(1); v = new(2);
                                             % 计算目标函数值的增量
       df = d(path(u-1),path(v)) + d(path(u),path(v+1)) - d(path(u-1),path(u)) - d(path(v),path(v+1));
       if df < 0                             % 接受准则
           path = [path(1:u-1), path(v:-1:u), path(v+1:n)];
           y = y + df;
       elseif exp(-df / K * T) > rand
           path = [path(1:u-1), path(v:-1:u), path(v+1:n)];
           y = y + df;
       end
       if y < bestY
           bestPath = path;
           bestY = y;
       end
    end
    T = T * coef;
end
fprintf('巡航路线 = ');                       % 打印巡航路径
for i = 1:size(bestPath, 2)
    fprintf('%d', bestPath(i));
    if i < size(bestPath, 2)
        fprintf(' ');
    else
        fprintf('\n');
    end
end
fprintf('巡航距离 = %f\n', bestY);            % 打印路径长度
xx = pos_X(bestPath); 
yy = pos_Y(bestPath);
plot(xx, yy, '->');                          % 绘制巡航路径

% path = [1 15 14 24 29 27 28 26 25 30 23 22 21 20 19 18 17 
%     16 12 11 13 7 6 5 4 2 8 10 9 3 31]
% y = 426.3058
