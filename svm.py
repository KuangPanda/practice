##虽然没实现但是也是自己做的 留个纪念以后弄懂再来改（flag）
# -*- coding: utf-8 -*-
import pandas as pd
import csv
import numpy as np
import random 
import re
import scipy.io as sio
import matplotlib.pyplot as plt

csv.field_size_limit(500 * 1024 * 1024)
filemail = pd.read_csv("F:\\train.csv")
test = pd.read_csv("f:\\test.csv")
spamdict = dict(filemail['content'][filemail['target']==1])
hamdict = dict(filemail['content'][filemail['target']==0])

#确定aj的值
def clipAlpha(aj,H,L):
        if aj > H:
            aj = H
        if L > aj:
            aj = L
        return aj

#i,j不能同时相等
def selectJrand(i,m):
    j = i
    while j == i:
        j = int(random.uniform(0,m))
    return j

#svm简单代码实现    
def simplesvm(dataMatIn,classLabels,toler,C,maxIter):
    dataMatrix = np.mat(dataMatIn);labelMat = np.mat(classLabels).transpose()
    b=0;m,n = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((m,1)))
    iter = 0
    while(iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fxi = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[i,:].T)) + b
            ei = fxi - float(labelMat[i])
            if((labelMat[i]*ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i,m)
                fxj = float(np.multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T)) + b
                ej = fxj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if(labelMat[i] != labelMat[j]):
                    L = max(0,alphas[j] - alphas[i])
                    H = min(C,C + alphas[j] - alphas[i])
                else:
                    L = max(0,alphas[j] + alphas[i] - C)
                    H = min(C,alphas[j] + alphas[i])
                #if L==H:print "L==H";continue
                eta = 2.0*dataMatrix[i,:]*dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - dataMatrix[j,:]*dataMatrix[j,:].T
                #if eta >= 0: print "eta>=0";continue
                alphas[j] -= labelMat[j]*(ei-ej)/eta
                alphas[j] = clipAlpha(alphas[j],H,L)
                #if(abs(alphas[j] - alphaJold) < 0.00001):
                 #   print "j not moving enough";continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - ei - labelMat[i]*(alphas[i] - alphaIold)*np.multiply(dataMatrix[i,:]*dataMatrix[i,:].T) - labelMat[j]*(alphas(j) - alphaJold)*np.multiply(dataMatrix[i,:]*dataMatrix[j,:].T)
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

#计算w的值
def calcw(alphas,dataArr,classLabels):
    X = np.mat(dataArr);labelMat = np.mat(classLabels).transpose()
    m,n = np.shape(X)
    w = np.zeros((n,1))
    for i in range(m):
        w+=np.multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w
    
#idea:先过滤去除字符长度小于2的词 字符长度大于6的词
#之后统计数据提取出现次数最多的前10个词作为该邮件的特征
#（y轴坐标位置)分别设置为x1,x2,....在以总词数作为另一特征(x轴坐标
#值作为其横坐  spam的类别标签为1 ham的类别标签为-1
#解析数据提取特征值
vocablist = list()
store = list()
count = dict()
            
#切割文本，统计词频
wordlist = []
spamcount = {}
spamlist = []
for key,value in spamdict.items():
    wordlist = re.split(r'\W*',value)
    for word in wordlist:
        if not spamcount.has_key(word):
            spamcount[word] = 1
            spamlist.append(word)
        else:
            spamcount[word] += 1

hamlist = []
hamcount = {}
for key,value in hamdict.items():
    wordlist = re.split(r'\W*',value)
    for word in wordlist:
        if not hamcount.has_key(word):
            hamcount[word] = 1
            hamlist.append(word)
        else:
            hamcount[word] += 1    

#提取垃圾邮件特征值 
sortedwordtfidf = sorted(hamcount.iteritems(),key=lambda asd:asd[1],reverse = True)
hamfeature1 = sortedwordtfidf[0:2]
hamfeature = list()
for word in hamfeature1:
    hamfeature.append(word[0]) 

sortedwordtfidf = sorted(spamcount.iteritems(),key=lambda asd:asd[1],reverse = True)
spamfeature1 = sortedwordtfidf[0:2]
spamfeature = list()
for word in spamfeature1:
    spamfeature.append(word[0])
    
X = list()
classlabel = list()
vecham = list()
for key,value in hamdict.items():
    wordlist = re.split(r'\W*',value)
    for word in hamfeature:
        if word in wordlist:
            vecham.append(1)
        else:
            vecham.append(0)
        X.append(vecham)
        classlabel.append(-1)

for key,value in spamdict.items():
   wordlist = re.split(r'\W*',value)
   for word in spamfeature:
        if word in wordlist:
            vecham.append(1)
        else:
            vecham.append(0)
        X.append(vecham)
        classlabel.append(1)
             
#测试
b,alphas = simplesvm(X,classlabel,0.0001,200,10)
w = calcw(alphas,wordlist,classlabel)
x = list()
for word in spamfeature:
    if word in test['content'][0]:
        x.append(1)
    else:
        x.append(0)
if sum(np.multiply(np.mat(w).transpose(),x)) + b > 1:
    print 'spam'
else:
    print 'ham'


#特征向量的提取方面有点问题 对公式ww^x+b的理解方面可能有点误差导致公式没能正确利用矩阵运算来解决问题。
