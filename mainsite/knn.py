#!/usr/bin/env Python
# coding=utf-8

from numpy import *
import operator


def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix('mainsite/static/files/knndata2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    d=[]
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],5)
        d.append('分类器预测临床疗效为： %d，实际为： %d' % (classifierResult,datingLabels[i]))
        if (classifierResult!=datingLabels[i]):
            errorCount+=1.0
    errorRate=errorCount/float(numTestVecs)
    erropercentage=errorRate*100
    return errorCount,d,erropercentage

def classifyPerson(ffMiles,iceCream,percentTats):
    resultList=['显效','有效','无效']
    percentTats=float(percentTats)
    ffMiles=float(ffMiles)
    iceCream=float(iceCream)
    datingDataMat,datingLabels=file2matrix('mainsite/static/files/knndata2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,5)
    res=resultList[classifierResult-1]
    return res

def file2matrix1(file):
    #fr=open(filename)
    arrayOLines=file.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector



def knnUpClassTest(file):
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix1(file)
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    d=[]
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],5)
        d.append('分类器预测为： %d，实际为： %d' % (classifierResult,datingLabels[i]))
        if (classifierResult!=datingLabels[i]):
            errorCount+=1.0
    errorRate=errorCount/float(numTestVecs)
    erropercentage=errorRate*100
    return errorCount,d,erropercentage