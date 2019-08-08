close all;
clear, clc;
%% ����GUI����
plot_button = uicontrol('style','pushbutton','string','����', 'fontsize',12, 'position',[150,400,50,20], 'callback', 'run=1;');
stop_button = uicontrol('style','pushbutton','string','ֹͣ','fontsize',12,'position',[250,400,50,20],'callback','freeze=1;');
quit_button = uicontrol('style','pushbutton','string','�˳�','fontsize',12,'position',[350,400,50,20],'callback','stop=1;close;');
num = uicontrol('style','text','string','1','fontsize',12, 'position',[20,400,50,20]);
%% Ԫ���Զ�������
n = 200;
%��ʼ����Ԫ��״̬
z = zeros(n,n);
sum = z;
cells = (rand(n, n)) < 0.6;
% ����ͼ����
img = image(cat(3, cells, z, z));
set(img, 'erasemode', 'none');
% Ԫ�����µ�����������
x = 2:n-1;
y = 2:n-1;
% Main Loop
stop= 0; run = 0;freeze = 0; 
while stop==0
    if run == 1
        % �����ھӴ�������
        sum(x,y) = cells(x,y-1) + cells(x,y+1) + cells(x-1, y) + cells(x+1,y)...
            + cells(x-1,y-1) + cells(x-1,y+1) + cells(x+1,y-1) + cells(x+1,y+1);
        % ���չ������
        cells = (sum == 3) | (sum == 2 & cells);
        set(img, 'cdata', cat(3, cells, z, z));
        stepnum = str2double(get(num, 'string'));
        set(num, 'string', num2str(stepnum));
    end
    if freeze == 1
        run = 0;
        freeze = 0;
    end
    drawnow; %drawnow - Update figure window and execute pending callbacks
end
