from math import sqrt,cos,sin,pi
import re

def precede(a,b):
    if a == '+' or a == '-':
        if b in ('+','-','?',')'):
            return 1
        else:
            return -1
    elif a == '*' or a == '/':
        if b in ('+','-','*','/',')','?'):
            return 1
        else:
            return -1
    elif a == '(':
        if b in (')'):
            return 0
        else:
            return -1
    elif a == ')':
        return 1;
    else:
        if b == '?':
            return 0
        else:
            return -1

def operate(a,theta,b):
    if theta == '+':
        return (float(a) + float(b))
    elif theta == '-':
        return (float(a) - float(b))
    elif theta == '*':
        return (float(a) * float(b))
    elif theta == '/':
        return (float(a) / float(b))

def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)

def multiply(n):
    index = n.find('^')
    index1 = int(n[:index])
    index2 = int(n[index+1:])
    return index1**index2
        
#获取输入
mystr = input()

#过滤sin
while mystr.find('sin') != -1:
    index1 = mystr.find('sin')
    index2 = mystr.find(')',index1)
    temp = mystr[index1:index2+1]
    mystr = mystr.replace(temp,str(eval(temp)))

#过滤cos
while mystr.find('cos') != -1:
    index1 = mystr.find('cos')
    index2 = mystr.find(')',index1)
    temp = mystr[index1:index2+1]
    mystr = mystr.replace(temp,str(eval(temp)))

mystr = list(mystr)
mylist = list()

#mylist中存放的的是分开的操作数和相应的运算符
for i in mystr:
    if i != ' ':
        mylist.append(i)

operation = ['+','-','*','/','(',')']

#my中存放的是运算符所在的位置
my = [-1]

#获取运算符所在的索引
for i,j in enumerate(mylist):
    if j in operation:
        my.append(i)

my.append(len(mylist))

#myoperation中存放的是所有的操作数已经转化为float型
myoperation1 = list()
mystr = str()

#将分割开的数字组成所需要的操作数
for i in range(0,len(my)-1):
    for j in range(my[i]+1,my[i+1]):
        mystr = mystr + mylist[j]
    myoperation1.append(mystr)
    mystr = str()

mynum = list()
for i in myoperation1:
    if len(i) != 0:
        mynum.append(i)

myoperation = list()
for i in mylist:
    if i in operation:
        myoperation.append(i)

#mytotal中存放的是过滤获得算术表达式
mytotal = list()
flag = 0

if len(myoperation) != 0 and myoperation[0] == '-':
    myoperation,mynum = mynum,myoperation 

while len(myoperation)!= 0 and len(mynum)!= 0:
    mytotal.append(mynum[0])
    mynum = mynum[1:]
    mytotal.append(myoperation[0])
    myoperation = myoperation[1:]
    if len(myoperation) == 0 or len(mynum) == 0:
        break
    if myoperation[0] == ')':
        mytotal.append(mynum[0])
        mynum = mynum[1:]
        mytotal.append(myoperation[0])
        myoperation = myoperation[1:]
        if len(myoperation) == 0:
            break
        while myoperation[0] == ')':
            mytotal.append(myoperation[0])
            myoperation = myoperation[1:]
        mytotal.append(myoperation[0])
        myoperation = myoperation[1:]
    if myoperation[0] == '(':
        mytotal.append(myoperation[0])
        myoperation = myoperation[1:]
        while myoperation[0] == '(':
            mytotal.append(myoperation[0])
            myoperation = myoperation[1:]
if len(mynum) == 1:
    mytotal.append(mynum[0])

for i,j in enumerate(mytotal):
    if type(j) == str and j[0] == 'v':
        mytotal[i] = str(sqrt(float(j[1:])))
    if type(j) == str and j[-1] == '!':
        mytotal[i] = str(fact(int(j[:-1])))
    if type(j) == str and  '^' in j:
        mytotal[i] = str(multiply(j))
  
operation = ['+','-','*','/','(',')','?']
mytotal.append('?')
#寄存运算符 
myoptr = ['?']
#寄存操作数或运算结果
myopnd = list()

c = mytotal[0]
while c != '?' or myoptr[-1] != '?':
    if c not in operation:
        myopnd.append(c)
        mytotal = mytotal[1:]
        c = mytotal[0]
    else:
        if precede(myoptr[-1],c) == -1:
            myoptr.append(c)
            mytotal = mytotal[1:]
            c = mytotal[0]
        elif precede(myoptr[-1],c) == 0:
            del myoptr[-1]
            mytotal = mytotal[1:]
            c = mytotal[0]
        else:
            theta = myoptr.pop()
            b = myopnd.pop()
            a = myopnd.pop()
            myopnd.append(operate(a,theta,b))

print (myopnd[0])
