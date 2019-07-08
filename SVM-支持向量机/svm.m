clc, clear
data=load('fenlei.txt');
data=data'; % Matrix8*30
X_train=data(2:end,1:27); % 训练数据集变量X
[X_train, ps]=mapstd(X_train); %数据标准化
X_unknown=data(2:end,28:end); % 待分类数据
X_unknown=mapstd('apply',X_unknown,ps); % 待分类数据的标准化
y_train=[ones(20,1);2*ones(7,1)]; % 训练数据集因变量y
s=svmtrain(X_train', y_train,'Method','SMO','Kernel_Function','linear'); % 训练SVM
sv_idx=s.SupportVectorIndices; % 返回支持向量的标号
coef=s.Alpha; % 返回分类函数的权系数
const_coef=s.Bias; % 返回分类函数的常数项
mean_and_std=s.ScaleData; %第1行返回的是已知样本点均值向量的相反数，第2行返回的是标准差向量的倒数
check=svmclassify(s,X_train');  % 验证训练集
err_rate=1-sum(y_train==check)/length(y_train);
ans=svmclassify(s,X_unknown'); % 对待判样本点进行分类
fprintf('label = (%d, %d, %d)\n', ans);
