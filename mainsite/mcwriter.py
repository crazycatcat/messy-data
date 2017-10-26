import nltk
import random
import jieba


file = open('mainsite/static/files/nj.txt', 'r',encoding='utf-8')         
walden = file.read()
walden = walden.replace('\n','')
walden = walden.replace(' ','')
walden=walden.replace('\u3000','')
walden=walden.replace('①','')
walden=walden.replace('￥','')
walden=walden.replace('⑤','')
walden=walden.replace('（','')
walden=walden.replace('）','')

walden= ' '.join(jieba.cut(walden))
walden = walden.split()
#print(walden)



def makePairs(arr):
    pairs = []
    for i in range(len(arr)):
        if i < len(arr)-1: 
            temp = (arr[i], arr[i+1])
            pairs.append(temp)
    return pairs
 
def generate(cfd, word = '人', num = 1000):
    text=''
    for i in range(num):
        arr = []                 # make an array with the words shown by proper count
        for j in cfd[word]:
            for k in range(cfd[word][j]):
                arr.append(j)
            #print(arr)
 
        #print(word, end='')
        text=text+word
        word = arr[int((len(arr))*random.random())]
    text=text+'...'
    return text

    
        

pairs = makePairs(walden)
cfd = nltk.ConditionalFreqDist(pairs)
#generate(cfd)
