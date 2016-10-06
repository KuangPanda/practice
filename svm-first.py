#svm 借用 machine learning in action
# -*- coding: utf-8 -*-
import pandas as pd
import math
import numpy
import random 

def clipAlpha(aj,H,L):
        if aj > H:
            aj = H
        if L > aj:
            aj = L
        return aj

def selectJrand(i,m):
    j = i
    while j == i:
        j = int(random.uniform(0,m))
    return j
    
def simplesvm(dataMatIn,classLabels,toler,C,maxIter):
    dataMatrix = mat(dataMatIn);labelMat = mat(classLabels).transpose()
    b=0;m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while(iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fxi = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            ei = fxi - float(labelMat[i])
            if((labelMat[i]*ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)
                fxj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                ej = fxj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if(labelMat[i] != labelMat[j]):
                    L = max(0,alphas[j] - alphas[i])
                    H = min(C,C + alphas[j] - alphas[i])
                else:
                    L = max(0,alphas[j] + alphas[i] - C)
                    H = min(C,alphas[j] + alphas[i])
                if L==H:print "L==H";continue
                eta = 2.0*dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                if eta >= 0: print "eta>=0";continue
                alphas[j] -= labelMat[j]*(ei-ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                if(abs(alphas[j] - alphaJold) < 0.00001):
                    print "j not moving enough";continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - ei - labelMat[i]*(alphas[i] - alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T - labelMat[j]*(alphas(j) - alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - ej - labelMat[i]*(alphas[i] - alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T - labelMat[j]*(alphas[j] - alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[j]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1+b2)/2.0
                alphaPairsChanged += 1
                print "iter:%d, i:%d,pairs changed %d" % (iter,i,alphaPairsChanged)
                if (alphaPairsChanged == 0): iter+=1
                else: iter = 0
                print "iteration number:%d" % iter
            return b,alphas  

def calcWs(alphas,dataArr,classLabels):
    X = mat(dataArr);labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w+=multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w
    
file = pd.read_csv("F:\\train.csv")

#idea:先过滤去除字符长度小于2的词 字符长度大于6的词
#之后统计数据提取出现次数最多的前10个词作为该邮件的特征
#（y轴坐标位置)分别设置为x1,x2,....在以总词数作为另一特征(x轴坐标
#值作为其横坐  spam的类别标签为1 ham的类别标签为-1

#解析数据提取特征值
vocablist = list()
store = list()
count = dict()
for i in range(2):
    email = file['content'][i]  #每一封邮件
    email = email.split()
    for word in email:
        if len(word) > 3 and len(word) < 6:
            if count.has_key(word.lower()) == False:
                count[word.lower()] = 1
            else:
                count[word.lower()] += 1
        store = count.values()
        store.sort()
        if file['target'][i] == 0:
            store.append(-1)
        else:
            store.append(1)
        store.append(len(sum
    vocablist.append(tuple(store[-11:]))
print vocablist

#测试代码正在修改  希望能改好
