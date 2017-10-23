#!/usr/bin/env Python
# coding=utf-8

import numpy as np
from collections import defaultdict
from operator import itemgetter
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import xlrd



wb = xlrd.open_workbook('mainsite/static/files/oner.xlsx')
wb=wb.sheets()[0]
nrows = wb.nrows
ncols = wb.ncols
X=[];Y=[]
for i in range(1, nrows):
    col =wb.row_values(i)
    col=col[1:]
    X.append(col[:-1]);Y.append(col[-1])
X=np.array(X)
y=np.array(Y)



n_samples, n_features = X.shape

#attribute_means=X.mean(axis=0)
#assert attribute_means.shape == (n_features,)
#X_d=np.array(X>=attribute_means,dtype='int')

def train_feature_value(X,y_true,feature,value):
    class_counts=defaultdict(int)
    for sample,y in zip(X,y_true):
        if sample[feature]==value:
            class_counts[y]+=1
    sorted_class_counts=sorted(class_counts.items(), key=itemgetter(1), reverse=True)
    most_frequent_class = sorted_class_counts[0][0]
    n_samples = X.shape[1]
    incorrect_predictions=[class_count for class_value, class_count in class_counts.items() if class_value != most_frequent_class]
    error=sum(incorrect_predictions)
    return most_frequent_class,error

def train(X, y_true, feature):
    n_samples, n_features = X.shape
    assert 0 <= feature < n_features    
    values = set(X[:,feature])
    predictors ={}
    errors = []
    for current_value in values:
        most_frequent_class, error = train_feature_value(X, y_true, feature, current_value)
        predictors[current_value] = most_frequent_class
        errors.append(error)
    total_error = sum(errors)
    return predictors, total_error

X_train,X_test,y_train,y_test=train_test_split(X,y)
numtr="随机划分出  {}  例纳入训练数据集".format(y_train.shape[0])
numte="随机划分出  {}  例纳入测试数据集（占总数的25%左右）".format(y_test.shape[0])


all_predictors = {variable: train(X_train, y_train, variable) for variable in range(X_train.shape[1])}
errors = {variable: error for variable, (mapping, error) in all_predictors.items()}
best_variable, best_error = sorted(errors.items(), key=itemgetter(1))[0]
#print("The best model is based on variable {0} and has error {1:.2f}".format(best_variable, best_error))

model = {'variable': best_variable,
         'predictor': all_predictors[best_variable][0]}
rule=model['predictor']

#variable=model['variable']
#predictor=model['predictor']
#prediction=predictor[int(sample[variable])]

def predict(X_test,model):
    variable=model['variable']
    predictor=model['predictor']
    y_predicted=np.array([predictor[sample[variable]] for sample in X_test])
    return y_predicted

y_predicted=predict(X_test,model)
#print(y_predicted)

accuracy=np.mean(y_predicted==y_test)*100
Accuracy="测试集预测准确率为 {:.1f}%".format(accuracy)
report=classification_report(y_test, y_predicted,digits=3)
report=report.replace('             precision','结局\t\t准确率')
report=report.replace('    recall','\t\t召回率')
report=report.replace('\n         ','\n')
report=report.replace('  f1-score','\t\tF1-score')
report=report.replace('e   support','e\t测试集中该分类的记录总数')
report=report.replace('       ','\t\t')
report=report.replace('      ','\t\t')
report=report.replace('avg / total','均值/总数')
#report=report.replace('\n\n','\n')
#precision准确率=被识别为该分类的正确分类记录数/被识别为该分类的记录数
#召回率=被识别为该分类的正确分类记录数/测试集中该分类的记录总数
#F1-score=2（准确率 * 召回率）/（准确率 + 召回率），F1-score是F-measure（又称F-score）beta=1时的特例。
#support=测试集中该分类的记录总数








