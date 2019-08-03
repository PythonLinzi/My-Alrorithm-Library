clear, clc;
n = 50;
m = 2000;
x = linspace(0, 1, n);        % λ��x����ָ�
t = linspace(0, 2, m);        % ʱ��t����ָ�
u = zeros(n, m);
dx = x(2) - x(1);             % ��λ����
dt = t(2) - t(1);             % ��λʱ��
for i = 1:n                   % ��ֵ���� u(x, 0) = sin(pi*x)
    u(i, 1) = sin(pi * x(i));
end
for j = 1:m                   % �߽�����1: u(0, t) = 0 
    u(1, j) = 0;              % ��߽�
end

for j = 1: m-1
    for i = 2:n
        if i == n             % �߽�����2: dudx(1,t) = -pi*exp(-t)
            u(i,j+1) = u(i-1,j+1) - pi * exp(-(t(j+1))) * dx;
        else
            u(i,j+1) = u(i,j) + dt * (u(i+1,j) - 2 * u(i, j) + u(i-1, j)) / ((pi * dx) ^ 2);
        end
    end
end
mesh(t, x, u);

