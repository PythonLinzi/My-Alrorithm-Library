clear, clc;
x = [1, 3, 6, 12, 19, 22, 23, 20, 21, 22.5, 40, 44, 42, 36, 39, 58, 62, 88, 90, 83, 71, 67, 64, 52, 84, 87, 71, 71, 58, 80, 1];
y = [99, 50, 64, 40, 41, 42, 37, 54, 60, 60.5, 26, 20, 35, 83, 95, 33, 30.5, 6, 38, 44, 42, 57, 59, 62, 65, 74, 70, 77, 68, 66, 99];
n = size(x,2);
d = zeros(n); %距离矩阵d初始化
for i=1:n-1
   for j=i+1:n
        d(i,j)=sqrt((x(i)-x(j))^2 + (y(i)-y(j))^2);
   end
end
d=d+d';
path=[];long=inf; %巡航路径及长度初始化
rand('state',sum(clock));  %初始化随机数发生器
for j=1:1000  %求较好的初始解
    path0=[1 1+randperm(n-2),n]; temp=0;
    for i=1:n-1
        temp=temp+d(path0(i),path0(i+1));
    end
    if temp<long
        path=path0; long=temp;
    end
end
e=0.1^30;L=20000;at=0.999;T=1;
for k=1:L  %退火过程
c=2+floor((n-2)*rand(1,2));  %产生新解
c=sort(c); c1=c(1);c2=c(2);
  %计算代价函数值的增量
df=d(path(c1-1),path(c2))+d(path(c1),path(c2+1))-d(path(c1-1),path(c1))-d(path(c2),path(c2+1));
  if df<0 %接受准则
  path=[path(1:c1-1),path(c2:-1:c1),path(c2+1:n)]; long=long+df;
  elseif exp(-df/T)>rand
  path=[path(1:c1-1),path(c2:-1:c1),path(c2+1:n)]; long=long+df;
  end
  T=T*at;
   if T<e
       fprintf('%d', k);
       break;
   end
end
path, long % 输出巡航路径及路径长度
xx=x(path);yy=y(path);
plot(xx,yy,'-*') %画出巡航路径
