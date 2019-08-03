clear, clc;
n = 50;
m = 2000;
x = linspace(0, 1, n);        % 位移x方向分割
t = linspace(0, 2, m);        % 时间t方向分割
u = zeros(n, m);
dx = x(2) - x(1);             % 单位步长
dt = t(2) - t(1);             % 单位时间
for i = 1:n                   % 初值条件 u(x, 0) = sin(pi*x)
    u(i, 1) = sin(pi * x(i));
end
for j = 1:m                   % 边界条件1: u(0, t) = 0 
    u(1, j) = 0;              % 左边界
end

for j = 1: m-1
    for i = 2:n
        if i == n             % 边界条件2: dudx(1,t) = -pi*exp(-t)
            u(i,j+1) = u(i-1,j+1) - pi * exp(-(t(j+1))) * dx;
        else
            u(i,j+1) = u(i,j) + dt * (u(i+1,j) - 2 * u(i, j) + u(i-1, j)) / ((pi * dx) ^ 2);
        end
    end
end
mesh(t, x, u);

