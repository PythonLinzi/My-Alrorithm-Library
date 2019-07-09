clc, clear
a=[-1 -2 0;-1 0 0];b=[-1;0];
[x,y]=ga(@ycfun1,3,a,b,[],[],[],[],@ycfun2);
x, y=-y
fprintf('\nansX = ');disp(x);
fprintf('ansY = %d\n', y);
% [x, y] = ga(@fitnessfunc, nvaes, A, b, Aeq, beq, LB, UB, @nonlcon, options)
% A*X <= b
% Aeq*X = beq
% LB<X<UB
% nonlcon: nonlinear constrains
