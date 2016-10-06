# -*- coding: utf-8 -*-
import pandas as pd
import csv
import math
csv.field_size_limit(500 * 1024 * 1024)
file = pd.read_csv("F:\\train.csv")

spamemail = file['content'][file['target']==1] #垃圾邮件
totalemail = file['content']  #总邮件

spamlist = list()  #垃圾邮件中的所有词
for email in spamemail:
    email = email.split()
    for word in email:
        if len(word) > 2 and len(word) < 10:
            spamlist.append(word.lower())
            
totallist = list()  #总邮件中的所有词
for email in totalemail:
    email = email.split()
    for word in email:
        if len(word) > 2 and len(word) < 10:
            totallist.append(word.lower())
            
#垃圾邮件，总邮件中独立出现的词            
spamvocablist = list(set(spamlist))  
totalvocablist = list(set(totallist))

#生成计词器
totalcount = dict.fromkeys(totalvocablist,0)
spamcount = dict.fromkeys(spamvocablist,0)

#统计数目
for word in spamlist:
    spamcount[word] += 1
for word in totallist:            
    totalcount[word] += 1
    
#计算单词的spam rating(log化方便后面乘法运算）
spamminess = dict.fromkeys(spamvocablist,0)
for word in spamvocablist:
    num1 = spamcount[word]*len(totallist)
    num2 = totalcount[word]*len(spamlist)
    spamminess[word] = math.log(float(num1)/float(num2))            

#P(spam)
must = math.log(float(1457)/float(6000))         

#统计正确的数目算精确度
n = 0
result = list()
testlist = list()

#test
test = pd.read_csv("F:\\test.csv")
for i in range(200):
    email = test['content'][i].split()
    for word in email:
        if len(word) > 2 and len(word) < 10:
           testlist.append(word.lower())
    chance = 0
    for word in email:
        if word in spamvocablist:
            chance+=spamminess[word]
        else:
            continue
    chance += must
    if chance < 0.5:
        #print "ham"
        result.append(0)
    else:
        #print "spam"
        result.append(1)
    if result[i] == test['target'][i]:
        n += 1   
print n       
print "precision",float(n)/float(200)  
#由于对近2000封邮件计算比较吃力所以这里只测试了200封试试效果    
