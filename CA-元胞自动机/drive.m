clear all;close all;clc
%% ���� button
plotbutton = uicontrol('style','pushbutton',...
    'string','Run', 'fontsize',12,...
    'position',[100,400,50,20], 'callback','run=1;');
stopbutton = uicontrol('style','pushbutton',...
    'string','Stop', 'fontsize',12,...
    'position',[300,400,50,20], 'callback','freeze=1;');
quit_button = uicontrol('style','pushbutton',...
    'string','�˳�','fontsize',12,...
    'position',[400,400,50,20],'callback','stop=1;close;');
num = uicontrol('style','text', 'string','1',...
    'fontsize',12, 'position',[20,400,50,20]);
%% CA Seting
z = zeros(38, 4);
cells = z;       %Ԫ������
p1 = 0.4;          %�������
p2 = 0.4;          %ת�����
t1 = 0;            %ʱ�����
t2 = 0;            %ʱ�����
% Initial Condition
cells(1, 1) = 1;
celss(1, 2) = 0;
cells(38, 3) = 0;
cells(38, 4) = 1;
run = 0; stop = 0; freeze = 0;
while true
    if run == 1
        for i = 1:37 %����
            if cells(i, 1) == 1 && cells(i, 2) == 0
                if rand() > p1
                    cells(i + 1, 1) = 0;
                    cells(i + 1, 2) = 1;
                else
                    cells(i + 1, 1) = 1;
                    cells(i + 1, 2) = 0;
                end
            end
            if cells(i, 1) == 0 && cells(i, 2) == 1
                if rand() > p1
                    cells(i + 1, 1) = 1;
                    cells(i + 1, 2) = 0;
                else
                    cells(i + 1, 1) = 0;
                    cells(i + 1, 2) = 1;
                end
            end
            if cells(i, 1) == 1 && cells(i, 2) == 1
                cells(i + 1, 1) = 1;
                cells(i + 1, 2) = 1;
            end
            if cells(i, 1) == 0 && cells(i, 2) == 0
                cells(i + 1, 1) = 0;
                cells(i + 1, 2) = 0;
            end
        end
        for i = 38:-1:2 %����
            if cells(i, 3) == 1 && cells(i, 4) == 0
                if rand() > p1
                    cells(i - 1, 3) = 0;
                    cells(i - 1, 4) = 1;
                else
                    cells(i - 1, 3) = 1;
                    cells(i - 1, 4) = 0;
                end
            end
            if cells(i, 3) == 0 && cells(i, 4) == 1
                if rand() > p1
                    cells(i - 1, 3) = 1;
                    cells(i - 1, 4) = 0;
                else
                    cells(i - 1, 3) = 0;
                    cells(i - 1, 4) = 1;
                end
            end
            if cells(i, 3) == 1 && cells(i, 4) == 1
                cells(i - 1, 3) = 1;
                cells(i - 1, 4) = 1;
            end
            if cells(i, 3) == 0 && cells(i, 4) == 0
                cells(i - 1, 3) = 0;
                cells(i - 1, 4) = 0;
            end
        end
        % show image
        [n, m] = size(cells);
        Area(1:n, 1:m, 1) = zeros(n, m);
        Area(1:n, 1:m, 2) = zeros(n, m);
        Area(1:n, 1:m, 3) = zeros(n, m);
        % ��ʾͼ��
        for i = 1:n
            for j = 1:m
                if cells(i, j) == 1
                    Area(i, j, :) = [255, 222, 0];
                elseif cells(i, j) == 0
                    Area(i, j, :) = [0, 90, 171];
                end
            end
        end
        Area = uint8(Area);
        Area = imagesc(Area);
        axis equal;
        axis tight;
        % �Ʋ�
        step_num = 1 + str2num(get(num, 'string'));
        set(num, 'string', num2str(step_num));
    end
    if freeze == 1
        run = 0;
        freeze = 0;
    end
    if stop == 1
        break
    end
    drawnow;
end
