clc, clear
fun3=@(x) -(x(1)^2+x(2)^2+3*x(3)^2+4*x(4)^2+2*x(5)^2-...
    8*x(1)-2*x(2)-3*x(3)-x(4)-2*x(5));
a=[1 1 1 1 1; 1 2 2 1 6; 2 1 6 0 0; 0 0 1 1 5];
b=[400 800 200 200]';
lb=zeros(5,1); ub=99*ones(5,1); 
Intcon=1:5;  %整数变量的下标
[x,y]=ga(fun3,5,a,b,[],[],lb,ub,[],Intcon);
fprintf('\nansX = ');disp(x);
fprintf('ansY = %d\n', -y);
% [x, y] = ga(@fitnessfunc, nvaes, A, b, Aeq, beq, LB, UB, @nonlcon, options)
% A*X <= b
% Aeq*X = beq
% LB<X<UB
% nonlcon: nonlinear constrains
