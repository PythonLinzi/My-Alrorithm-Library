%************************************
%求解一维热传导偏微分方程的一个综合函数程序
%************************************
m = 0;
x = linspace(0, 1, 20); %xmesh
t = linspace(0, 2, 20); %tspan
%************
%以 pde 求解
%************
sol = pdepe(m, @func_20_1, @ic20_1, @bc20_1, x, t);
u = sol(:,:,1); %取出答案
%************
%绘图输出
%************
figure(1);
surf(x, t, u);
title('pde数值解');
xlabel('位置 x')
ylabel('时间 t' )
zlabel('数值解 u')
%*************
%与解析解做比较
%*************
figure(2);
surf(x, t, exp(-t)' * sin(pi * x));
title('解析解')
xlabel('位置 x')
ylabel('时间 t' )
zlabel('数值解 u')
%*****************
%t=tf=2 时各位置之解
%*****************
figure(3);
M = length(t); %取终点时间的下表
xout = linspace(0,1,100); %输出点位置
[uout,dudx] = pdeval(m, x, u(M,:), xout);
plot(xout,uout); %绘图
title('时间为 2 时,各位置下的解');
xlabel('x');
ylabel('u');
size(u)
size(x)
size(t)
