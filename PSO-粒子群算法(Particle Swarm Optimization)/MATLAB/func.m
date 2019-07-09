function [y] = func(x)
    y = x(1) * x(1) + x(2) * x(2) + x(3) * x(3) + 8;
    % 采用罚函数法将约束条件加入目标函数
    penalty = 1e7;
    if -x(1) > 0
        y = y + penalty * (-x(1));
    end
    if -x(2) > 0
        y = y + penalty * (-x(2));
    end
    if -x(3) > 0
        y = y + penalty * (-x(3));
    end
    % -x1^2 + x2 - x3^2 <= 0
    bnds = -x(1) * x(1) + x(2) - x(3) * x(3);
    if bnds > 0
        y = y + penalty * bnds;
    end
    % x1 + x2^2 + x3^2 - 20 <= 0
    bnds = x(1) + x(2) * x(2) + x(3) * x(3) - 20;
    if bnds > 0
        y = y + penalty * bnds;
    end
    % -x1 - x2^2 + 2 <= 0
    bnds = -x(1) - x(2) * x(2) + 2;
    if bnds > 0
        y = y + penalty * bnds;
    end
    % -x2 - 2 * x3^2 + 3 <= 0
    bnds = -x(2) - 2 * x(3) * x(3) + 3;
    if bnds > 0
        y = y + penalty * bnds;
    end
end
