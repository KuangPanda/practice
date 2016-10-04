# -*- coding: utf-8 -*-
#使用贝叶斯对垃圾邮件进行分类的过程
#1.收集数据：对csv文件进行操作
#2.准备数据：将csv文件解析成词条向量
#3.分析数据：检查词条确保解析的正确性
#4.训练算法：
#5.测试算法：构建一个新的测试函数来计算文档集的错误率
#6.使用算法：构建一个完整的程序对一组文档进行分类，将错分的文档输出到屏幕上
import pandas as pd
import csv

wordlist = pd.read_csv("train.csv")
spamemail = wordlist['content'][wordlist['target']==1] #垃圾邮件
hamemail = wordlist['content'][wordlist['target']==0]  #非垃圾邮件

#1.创建一个包含在所有文档中出现的不重复词的列表
def CreateVocabList(dataset):
    vocabset = set([])
    for document in dataset:
        vocabset = vocabset | set(document)
        return list(vocabset)

#2.切分数据
#def TextParse(inputset):
#    import re
#    token = re.split(r'\W*',inputset)
#    outputset = [tok.lower() for tok in token if len(tok) > 2]
#    return outputset

spamvocablist = CreateVocabList(spamemail) #垃圾邮件中出现的所有词条
hamvocablist = CreateVocabList(hamemail)   #非垃圾邮件中出现的所有词条

#3.计算所有垃圾邮件中每个词出现的次数
def SpamWordCount(spamvocablist,spamemail):
    spamcount = dict().fromkeys(spamvocablist)  #生成字典
    for word in spamvocablist:
        spamcount[word] = 0           #初始化字典中的值
    for word in spamemail:
        if word in spamvocablist:
            spamcount[word] += 1  #计算垃圾邮件中每个词出现的次数
    return spamcount

spamcount = SpamWordCount(spamvocablist,spamemail)

#4.计算所有非垃圾邮件中每个词出现的次数
def HamWordCount(hamvocablist,hamemail):
    hamcount = dict().fromkeys(hamvocablist)    #生成字典
    for word in hamvocablist:
        hamcount[word] = 0           #初始化字典中的值
    for word in hamemail:
        if word in hamvocablist:     
            hamcount[word] += 1     #计算非垃圾邮件中每个词出现的次数
    return hamcount

hamcount = HamWordCount(hamvocablist,hamemail)

#5.计算spamminess
def Spamminess(spamvocablist,spamcount,hamcount):
    spamminess = dict().formkeys(spamvocablist)
    for word in spamvocablist:
        spamminess[word] = (spamcount[word])/(spamcount[word] + hamcount[word])
    return spamminess

spamminess = Spamminess(spamvocablist,spamcount,hamcunt)

#6.计算hamminess
def Hamminess(hamvocablist,spamcount,hamcount):
    hamminess = dict().fromkeys(hamvocablist)
    for word in hamvocablist:
        hamminess[word] = (hamcount[word])/(spamcount[word] + hamcount[word])
    return hamminess

hamminess = Hamminess(hamvocablist,spamcount,hamcount)

testemail = pd.read_csv('test.csv')

#7.测试
def test(testemail):
    spam = 1; ham = 1;
    for index in range(200):
        for word in testemail[index]['content']:
            spam = spam * spamminess[word]
            ham = ham * hamminess[word]
        if spam >= ham:
            print 'The %dth Test Email is Spam Email' % i
        else:
            print 'The %dth Test Email is Non-Spam Email' % i
    
#对csv文件的处理正在处理中 以上代码参照机器学习实战和朴素贝叶斯想法而成  可能执行效率低但这是初版
