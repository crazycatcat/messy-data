#!/usr/bin/env Python
# coding=utf-8
from numpy import *

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)   #initialize to all ones
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not 
            randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest(ff):
    #frTrain = open(); frTest = open()
    #x=ff.readlines()
    trainingSet = []; trainingLabels = []
    for line in ff:
        #line=unicode(line,'utf8')
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(20):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent1(array(trainingSet), trainingLabels, 1000)
    errorCount = 0; numTestVec = 0.0
    for line in ff:
        #line=unicode(line,'utf8')
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr =[]
        for i in range(20):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
            errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    x="本次测试错误率为: %f" % errorRate
    return errorRate,x

def multiTest(f):
    
    ff=f#[line for line in f.readlines()]
    numTests =5; errorSum=0.0
    y=[]
    for k in range(numTests):
        errorSum += colicTest(ff)[0]
        y=y.append(colicTest(ff)[1])
    a="在经过 %d 次迭代后平均错误率为: %f" % (numTests, errorSum/float(numTests))
    return y,a
