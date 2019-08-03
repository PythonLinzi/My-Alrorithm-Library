%************************************
%���һά�ȴ���ƫ΢�ַ��̵�һ���ۺϺ�������
%************************************
m = 0;
x = linspace(0, 1, 20); %xmesh
t = linspace(0, 2, 20); %tspan
%************
%�� pde ���
%************
sol = pdepe(m, @func_20_1, @ic20_1, @bc20_1, x, t);
u = sol(:,:,1); %ȡ����
%************
%��ͼ���
%************
figure(1);
surf(x, t, u);
title('pde��ֵ��');
xlabel('λ�� x')
ylabel('ʱ�� t' )
zlabel('��ֵ�� u')
%*************
%����������Ƚ�
%*************
figure(2);
surf(x, t, exp(-t)' * sin(pi * x));
title('������')
xlabel('λ�� x')
ylabel('ʱ�� t' )
zlabel('��ֵ�� u')
%*****************
%t=tf=2 ʱ��λ��֮��
%*****************
figure(3);
M = length(t); %ȡ�յ�ʱ����±�
xout = linspace(0,1,100); %�����λ��
[uout,dudx] = pdeval(m, x, u(M,:), xout);
plot(xout,uout); %��ͼ
title('ʱ��Ϊ 2 ʱ,��λ���µĽ�');
xlabel('x');
ylabel('u');
size(u)
size(x)
size(t)
