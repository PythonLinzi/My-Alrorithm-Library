function ti12_1
fun1=@(x) (x(1)-2)^2+(x(2)-1)^2;
a=[-1,2]; b=1;
[x, y] = ga(fun1,2,a,b,[],[],[],[],@fun2);
fprintf('\nansX = ');disp(x);
fprintf('ansY = %d\n', y);
function [c,ceq]=fun2(x)
c=-x(1)^2/4+x(2)^2-1; ceq=[];
% [x, y] = ga(@fitnessfunc, nvars, A, b, Aeq, beq, LB, UB, @nonlcon, options)
% A*X <= b
% Aeq*X = beq
% LB<X<UB
% nonlcon: nonlinear constrains
