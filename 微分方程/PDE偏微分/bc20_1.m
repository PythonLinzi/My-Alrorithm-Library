function [pl, ql, pr, qr] = bc20_1(xl, ul, xr, ur, t)
pl = ul;
ql = 0;
pr = pi * exp(-t);
qr = 1;
end
