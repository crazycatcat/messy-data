import numpy as np
from collections import defaultdict
import xlrd

wb = xlrd.open_workbook('mainsite/static/files/affinity_dataset2.xlsx')
wb=wb.sheets()[0]
nrows = wb.nrows
ncols = wb.ncols
data=[]
for i in range(1, nrows):
    col =wb.row_values(i)
    col=col[1:]
    data.append(col)
features=wb.row_values(0)
features=features[1:]
X=np.array(data)

n_samples, n_features = X.shape

vaild_rules=defaultdict(int)
invaild_rules=defaultdict(int)
num_occurances=defaultdict(int)


for sample in X:
    for premise in range(n_features):
        if sample[premise]==0:continue
        num_occurances[premise]+=1
        for conclusion in range(n_features):
            if premise==conclusion:continue
            if sample[conclusion]==1:
                vaild_rules[(premise,conclusion)]+=1
            else:
                invaild_rules[(premise,conclusion)]+=1

support=vaild_rules
confidence=defaultdict(float)
for premise,conclusion in vaild_rules.keys():
    rule=(premise,conclusion)
    confidence[rule]=vaild_rules[rule]/num_occurances[premise]
    
def print_rule(premise,conclusion,support,confidence,features):
    premise_name=features[premise]
    conclusion_name=features[conclusion]
    res="选择  {0}穴  的同时也会选择 {1}穴。   - 支持度：{2}\n - 置信度：{3:.3f}\n".format(premise_name,conclusion_name,support[(premise,conclusion)],confidence[(premise,conclusion)])
    return res

from operator import itemgetter
def sortsupp():
    sorted_support=sorted(support.items(),key=itemgetter(1),reverse=True)
    suppres=[]
    for index in range(5):
        i="规则 #{0}\n".format(index+1)
        premise,conclusion=sorted_support[index][0]
        #premise=0
        suppres.append(i+print_rule(premise,conclusion,support,confidence,features))
    return suppres
    
def sortconf():
    sorted_confidence=sorted(confidence.items(),key=itemgetter(1),reverse=True)
    confres=[]
    for index in range(5):
        i="规则 #{0}\n".format(index+1)
        premise,conclusion=sorted_confidence[index][0]
        #premise=0
        confres.append(i+print_rule(premise,conclusion,support,confidence,features))
    return confres