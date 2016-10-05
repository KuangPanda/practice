# -*- coding: utf-8 -*-
import pandas as pd
import csv
import math
csv.field_size_limit(500 * 1024 * 1024)
file = pd.read_csv("F:\\train.csv")

 #1.解析数据 
spamemail = file['content'][file['target']==1] #垃圾邮件
hamemail = file['content'][file['target']==0]  #非垃圾邮件

#2.创建所有出现在垃圾邮件中的单词
spamlist = list()
for email in spamemail:
    email = email.split()
    for word in email:
        if len(word) > 2 and len(word) < 10:
            spamlist.append(word.lower())
            
#3.创建所有出现在非垃圾邮件中的单词
hamlist = list()
for email in hamemail:
    email = email.split()
    for word in email:
        if len(word) > 2 and len(word) < 10:
            hamlist.append(word.lower())

#4.创建相应的词库
hamvocablist = list(set(hamlist))
spamvocablist = list(set(spamlist))
allword = list()
allword.extend(spamvocablist)
allword.extend(hamvocablist)

#5.统计单词出现的次数
spamcount = dict.fromkeys(spamvocablist,0)
hamcount = dict.fromkeys(hamvocablist,0)
for word in spamlist:
        spamcount[word] += 1
for word in hamlist:
        hamcount[word] += 1

#6.计算每个单词的rating
spamminess = dict.fromkeys(allword,0)
hamminess = dict.fromkeys(allword,0)
for word in allword:
    if word in spamlist and word in hamlist:
     #   if spamcount[word] != 0 and hamcount[word] != 0:
         spamminess[word] = float(spamcount[word])/float(spamcount[word]+hamcount[word])
    #if hamcount[word] != 0:
         hamminess[word] = float(hamcount[word])/float(spamcount[word] + hamcount[word])
  
#7.实验
testlist = list()
test = pd.read_csv("F:\\test.csv")
for i in range(20):
    email = test['content'][i].split()
    for word in email:
        if len(word) > 2 and len(word) < 10:
           testlist.append(word.lower())
    chance = 0
    for word in testlist:
        if word in spamvocablist and word in hamvocablist:
           chance = math.log(float(spamminess[word])/float(haminess[word]))
    if chance < 0:
        print "ham"
    if chance > 0:
        print "spam"
