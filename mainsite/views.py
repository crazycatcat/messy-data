#!/usr/bin/env Python
# coding=utf-8
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Charpter,Item,itemEntry,Statistic,DataMining,DataLab

from django.http import HttpResponseRedirect,Http404,HttpResponse

from django.core.urlresolvers import reverse

from .forms import ItemForm,itemEntryForm,UploadExcelForm

from django.contrib.auth.decorators import login_required

from django.template.loader import get_template

from numpy import mean,median,var,std,ptp
import numpy as np

import matplotlib

matplotlib.use('Agg')

from matplotlib.figure import Figure                      
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

from scipy.stats import kstest,levene,ttest_1samp,ttest_rel,ttest_ind,chi2_contingency,fisher_exact
from .knn import *
from .biologists import *
from .apriori import *
import codecs,decTree
import xlrd,copy
from django.core.files.uploadedfile import InMemoryUploadedFile


# Create your views here.

def index(request):
    return render(request,'mainsite/index.html')
	
def charpters(request):
    #charpters=Charpter.objects.all()
    #charpter_lists=list()
    #for count,charpter in enumerate(charpters):
        #charpter_lists.append("No.{}:".format(str(count))+str(charpter)+"<br>")
    #return HttpResponse(charpter_lists)
    charpters=Charpter.objects.order_by('pub_date')
    context={'charpters':charpters}
    return render(request,'mainsite/charpters.html',context)

@login_required	
def items(request):
    items=Item.objects.filter(owner=request.user).order_by('pub_date')
    context={'items':items}
    return render(request,'mainsite/items.html',context)
	
def charpter(request,charpter_id):
    charpter=Charpter.objects.get(id=charpter_id)
    entries=charpter.charpterentry_set.order_by('-pub_date')
    context={'charpter':charpter,'entries':entries}
    return render(request,'mainsite/charpter.html',context)

@login_required	
def item(request,item_id):
    item=Item.objects.get(id=item_id)
    if item.owner !=request.user:
	raise Http404
    entries=item.itementry_set.order_by('-pub_date')
    context={'item':item,'entries':entries}
    return render(request,'mainsite/item.html',context)

@login_required	
def new_item(request):
    if request.method!='POST':
	form=ItemForm()
    else:
	form=ItemForm(request.POST)
	if form.is_valid():
	    new_item=form.save(commit=False)
	    new_item.owner=request.user
	    new_item.save()
	    return HttpResponseRedirect(reverse('mainsite:items'))
	
    context={'form':form}
    return render(request,'mainsite/new_item.html',context)

@login_required
def new_itementry(request,item_id):
    item=Item.objects.get(id=item_id)
    if request.method!='POST':
	form=itemEntryForm()
    else:
	form=itemEntryForm(data=request.POST)
	if form.is_valid():
	    new_itementry=form.save(commit=False)
	    new_itementry.item=item
	    new_itementry.save()
	    return HttpResponseRedirect(reverse('mainsite:item',args=[item_id]))
	
    context={'item':item,'form':form}
    return render(request,'mainsite/new_itementry.html',context)

@login_required
def edit_itementry(request,itementry_id):
    entry=itemEntry.objects.get(id=itementry_id)
    item=entry.item
    if item.owner !=request.user:
	raise Http404
    if request.method!='POST':
	form=itemEntryForm(instance=entry)
    else:
	form=itemEntryForm(instance=entry,data=request.POST)
	if form.is_valid():
	    form.save()
	    return HttpResponseRedirect(reverse('mainsite:item',args=[item.id]))
	
    context={'entry':entry,'item':item,'form':form}
    return render(request,'mainsite/edit_itementry.html',context)

def statistics(request):
    statistics=Statistic.objects.order_by('pub_date')
    context={'statistics':statistics}
    return render(request,'mainsite/statistics.html',context)

def dataminings(request):
    dataminings=DataMining.objects.order_by('pub_date')
    context={'dataminings':dataminings}
    return render(request,'mainsite/dataminings.html',context)

def datalabs(request):
    datalabs=DataLab.objects.order_by('pub_date')
    context={'datalabs':datalabs}
    return render(request,'mainsite/datalabs.html',context)

def desstat(request):
    return render(request,'mainsite/desstat.html')


	
def result(request):
    
	#template=get_template('desstat.html')
    '''requestData=request.GET.copy()
    data=requestData['user_data']
    data=data.encode('utf-8')
    
    datanum=[]
    for i in data.split(' '):
	datanum.append(int(i))
    
    total=sum(datanum)
    datamean=round(mean(datanum),3)
    datamedian=round(float(median(datanum)),3)
    datarange=round(ptp(datanum),3)
    datavar=round(var(datanum),3)
    datastd=round(std(datanum),3)
    datacv=round((datastd/datamean*100),3)

    knnfile = request.FILES.get('knnfile', None)
    f = open(os.path.join('mainsite/static/userfiles/', knnfile.name), 'wb+')
    for chunk in knnfile.chunks():
        f.write(chunk)
    errorCount,ds,erropercentage=knnUpClassTest(str('mainsite/static/userfiles/'+knnfile.name))
    context={'erropercentage':erropercentage,'ds':ds}
    f.close()
    os.remove(os.path.join('mainsite/static/userfiles/', knnfile.name))
    return render(request,'mainsite/knnupres.html',context)
    context={'data':data,'datamean':datamean,'datamedian':datamedian,'datarange':datarange,'datavar':datavar,'datastd':datastd,'datacv':datacv}
    return render(request,'mainsite/result.html',context)'''
    form = UploadExcelForm(request.POST, request.FILES)
    if form.is_valid():
        wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read()) # 关键点在于这里
    data=[]
    table = wb.sheets()[0]
    row = table.nrows
    
    for i in xrange(1, row):
        col = table.row_values(i)
        data.append(col)
    datanum=[]
    for i in range(0,len(data)):
        datanum.append(data[i][0])

    total=sum(datanum)
    datamean=round(mean(datanum),3)
    datamedian=round(float(median(datanum)),3)
    datarange=round(ptp(datanum),3)
    datavar=round(var(datanum),3)
    datastd=round(std(datanum),3)
    datacv=round((datastd/datamean*100),3)
    context={'data':data,'datamean':datamean,'datamedian':datamedian,'datarange':datarange,'datavar':datavar,'datastd':datastd,'datacv':datacv}
    return render(request,'mainsite/result.html',context)



@login_required
def boxplot(request):
    requestData=request.GET.copy()
    data=requestData['user_data']
    data=data.encode('utf-8')
     
    datanum=[]
    for i in data.split(' '):
	datanum.append(int(i))
    datanum=list(datanum)
    fig=Figure(figsize=(6,6))
    ax=fig.add_subplot(111)
    ax.boxplot(datanum)
    canvas=FigureCanvasAgg(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)
    return response

@login_required	
def hist(request):
	#template=get_template('desstat.html')
    requestData=request.GET.copy()
    data=requestData['user_data']
    data=data.encode('utf-8')
    datanum=[]
    for i in data.split(' '):
	datanum.append(int(i))
    datanum=list(datanum)
    fig=Figure(figsize=(6,6))
    ax=fig.add_subplot(111)
    ax.hist(datanum)
    
    canvas=FigureCanvasAgg(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.close(fig)
    return response

def normtest(request):
    return render(request,'mainsite/normtest.html')
	
def normresult(request):
    requestData=request.GET.copy()
    data=requestData['user_data']
    data=data.encode('utf-8')
    datanum=[]
    for i in data.split(' '):
	datanum.append(int(i))
    datanum=list(datanum)
    res=kstest(datanum, 'norm')
    z=round(float(res[0]),4)
    p=round(float(res[1]),4)
    context={'data':data,'z':z,'p':p}
    return render(request,'mainsite/normresult.html',context)
	
def sdtest(request):
    return render(request,'mainsite/sdtest.html')
	
def sdtestresult(request):
    requestData=request.GET.copy()
    data1=requestData['user_data1']
    data1=data1.encode('utf-8')
    datanum1=[]
    for i in data1.split(' '):
	datanum1.append(int(i))
    datanum1=list(datanum1)
	
    requestData=request.GET.copy()
    data2=requestData['user_data2']
    data2=data2.encode('utf-8')
    datanum2=[]
    for i in data2.split(' '):
	datanum2.append(int(i))
    datanum2=list(datanum2)
	
    res=levene(datanum1,datanum2,center = 'trimmed')
    f=round(float(res[0]),4)
    p=round(float(res[1]),4)
    context={'data1':data1,'data2':data2,'f':f,'p':p}
    return render(request,'mainsite/sdtestresult.html',context)
	
def knn(request):
    return render(request,'mainsite/knn.html')

@login_required
def knntest(request):
    errorCount,ds,erropercentage=datingClassTest()
    context={'erropercentage':erropercentage,'ds':ds}
    return render(request,'mainsite/knntest.html',context)

@login_required
def knntouch(request):
    requestData=request.GET.copy()
    ffMiles=requestData['hours']
    iceCream=requestData['kgs']
    percentTats=requestData['percentage']
    ffMiles1=ffMiles.encode('utf-8')
    iceCream1=iceCream.encode('utf-8')
    percentTats1=percentTats.encode('utf-8')
    res=classifyPerson(ffMiles1,iceCream1,percentTats1)
    context={'res':res,'ffMiles1':ffMiles1,'iceCream1':iceCream1,'percentTats1':percentTats1}
    return render(request,'mainsite/knntouch.html',context)
	
def dttest(request):
    return render(request,'mainsite/dttest.html')
	
def dttestres(request):
    requestData=request.GET.copy()
    data1=requestData['user_data1']
    data1=data1.encode('utf-8')
    datanum1=[]
    for i in data1.split(' '):
	datanum1.append(int(i))
    datanum1=list(datanum1)
	
    requestData=request.GET.copy()
    data2=requestData['user_data2']
    data2=data2.encode('utf-8')
    datanum2=[]
    datanum2.append(int(data2))
    datanum2=list(datanum2)
    
    res=ttest_1samp(datanum1,popmean=datanum2)
    t=round(float(res[0]),4)
    p=round(float(res[1]),4)
    context={'data1':data1,'data2':data2,'t':t,'p':p}
    return render(request,'mainsite/dttestres.html',context)
	
def pttest(request):
    return render(request,'mainsite/pttest.html')
	
def pttestres(request):
    requestData=request.GET.copy()
    data1=requestData['user_data1']
    data1=data1.encode('utf-8')
    datanum1=[]
    for i in data1.split(' '):
	datanum1.append(int(i))
    datanum1=list(datanum1)
	
    requestData=request.GET.copy()
    data2=requestData['user_data2']
    data2=data2.encode('utf-8')
    datanum2=[]
    for i in data2.split(' '):
	datanum2.append(int(i))
    datanum2=list(datanum2)
    
    res=ttest_rel(datanum1,datanum2)
    t=round(float(res[0]),4)
    p=round(float(res[1]),4)
    context={'data1':data1,'data2':data2,'t':t,'p':p}
    return render(request,'mainsite/pttestres.html',context)
	
def upttest(request):
    return render(request,'mainsite/upttest.html')
	
def upttestres(request):
    requestData=request.GET.copy()
    data1=requestData['user_data1']
    data1=data1.encode('utf-8')
    datanum1=[]
    for i in data1.split(' '):
	datanum1.append(int(i))
    datanum1=list(datanum1)
	
    requestData=request.GET.copy()
    data2=requestData['user_data2']
    data2=data2.encode('utf-8')
    datanum2=[]
    for i in data2.split(' '):
	datanum2.append(int(i))
    datanum2=list(datanum2)
    
    res=ttest_ind(datanum1,datanum2)
    t=round(float(res[0]),4)
    p=round(float(res[1]),4)
    context={'data1':data1,'data2':data2,'t':t,'p':p}
    return render(request,'mainsite/upttestres.html',context)
	
def attest(request):
    return render(request,'mainsite/attest.html')
	
def attestres(request):
    requestData=request.GET.copy()
    data1=requestData['user_data1']
    data1=data1.encode('utf-8')
    datanum1=[]
    for i in data1.split(' '):
	datanum1.append(int(i))
    datanum1=list(datanum1)
	
    requestData=request.GET.copy()
    data2=requestData['user_data2']
    data2=data2.encode('utf-8')
    datanum2=[]
    for i in data2.split(' '):
	datanum2.append(int(i))
    datanum2=list(datanum2)
    
    res=ttest_ind(datanum1,datanum2,equal_var=False)
    t=round(float(res[0]),4)
    p=round(float(res[1]),4)
    context={'data1':data1,'data2':data2,'t':t,'p':p}
    return render(request,'mainsite/attestres.html',context)

@login_required
def caa(request):
    return render(request,'mainsite/caa.html')

@login_required
def caares(request):
    requestData=request.GET.copy()
    seq=requestData['user_data']
    seq=seq.encode('utf-8')
    seq=seq.upper()
    ress=count_aminoacids(seq)
    context={'seq':seq,'ress':ress}
    return render(request,'mainsite/caares.html',context)
	
@login_required
def cdna(request):
    return render(request,'mainsite/cdna.html')

@login_required
def cdnares(request):
    requestData=request.GET.copy()
    seq=requestData['user_data']
    seq=seq.encode('utf-8')
    seq=seq.upper()
    ress=count_dna(seq)
    context={'seq':seq,'ress':ress}
    return render(request,'mainsite/cdnares.html',context)

@login_required
def crna(request):
    return render(request,'mainsite/crna.html')

@login_required
def crnares(request):
    requestData=request.GET.copy()
    seq=requestData['user_data']
    seq=seq.encode('utf-8')
    seq=seq.upper()
    ress=count_rna(seq)
    context={'seq':seq,'ress':ress}
    return render(request,'mainsite/crnares.html',context)
	
def chiq(request):
    return render(request,'mainsite/chiq.html')
	
def chiqres(request):
    requestData=request.GET.copy()
    a=requestData['a'].encode('utf-8')
    b=requestData['b'].encode('utf-8')
    c=requestData['c'].encode('utf-8')
    d=requestData['d'].encode('utf-8')
    a,b,c,d,=int(a),int(b),int(c),int(d)
    l=[a+c,b+d]
    l2=[a+b,c+d]
    t=round((float(min(l)*min(l2))/(a+b+c+d)),2)
    
    d=np.array([[a,b],[c,d]])
    res=chi2_contingency(d,correction=False)
    x2=round(res[0],4)
    p=round(res[1],4)
    context={'t':t,'x2':x2,'p':p}
    return render(request,'mainsite/chiqres.html',context)
	
def fisher(request):
    return render(request,'mainsite/fisher.html')
	
def fisherres(request):
    requestData=request.GET.copy()
    a=requestData['a'].encode('utf-8')
    b=requestData['b'].encode('utf-8')
    c=requestData['c'].encode('utf-8')
    d=requestData['d'].encode('utf-8')
    a,b,c,d,=int(a),int(b),int(c),int(d)
    l=[a+c,b+d]
    l2=[a+b,c+d]
    t=round((float(min(l)*min(l2))/(a+b+c+d)),2)
    f1=[a,b]
    f2=[c,d]
    res=fisher_exact([f1,f2])
    #d=np.array([[a,b],[c,d]])
    #res=chi2_contingency(d)
    oddsratio=round(res[0],4)
    p=round(res[1],4)
    context={'t':t,'oddsratio':oddsratio,'p':p}
    return render(request,'mainsite/fisherres.html',context)
	
def apdie(request):
    return render(request,'mainsite/apdie.html')
	
@login_required
def apdieres(request):
    apdieDataSet=[line.split(',') for line in open('mainsite/static/files/apdie.csv').readlines()]
    '''apdieDataSet=[]
    with open('mainsite/static/files/apdie.csv') as f:
        for line in f.readlines():
            #line=unicode(line,"utf8")
            line=line.strip('\n')
            line=line.split(',')
            apdieDataSet.append(line)'''
    L,suppData=apriori(apdieDataSet,minSupport=0.3)
    res2s=[]
    for item in L[1]:
	if item.intersection(['Death']):
	    res2s.append(item)
    res3s=[]
    for item in L[2]:
	if item.intersection(['Death']):
	    res3s.append(item)
    res4s=[]
    for item in L[3]:
	if item.intersection(['Death']):
	    res4s.append(item)
    context={'res2s':res2s,'res3s':res3s,'res4s':res4s}
    #context={'apdieDataSet':apdieDataSet[0]}
    return render(request,'mainsite/apdieres.html',context)

def appoint(request):
    return render(request,'mainsite/appoint.html')
	
@login_required
def appointres(request):
    appointDataSet=[line.split(',') for line in open('mainsite/static/files/appoint.csv').readlines()]
    '''apdieDataSet=[]
    with open('mainsite/static/files/apdie.csv') as f:
        for line in f.readlines():
            #line=unicode(line,"utf8")
            line=line.strip('\n')
            line=line.split(',')
            apdieDataSet.append(line)'''
    L,suppData=apriori(appointDataSet,minSupport=0.6)
    rules=generateRules(L,suppData,minConf=0.5)
    L1,suppData1=apriori(appointDataSet,minSupport=0.4)
    rules1=generateRules(L1,suppData1,minConf=0.4)
    context={'rules2':rules[:12],'rules3':rules[12:24],'rules4':rules[24:],'rules1':rules1}
    #context={'apdieDataSet':apdieDataSet[0]}
    return render(request,'mainsite/appointres.html',context)
	
def id3(request):
    return render(request,'mainsite/id3.html')
	
@login_required
def id3res(request):
    #apdieDataSet=[line.split(',') for line in open('mainsite/static/files/id3.txt').readlines()]
   
    lense=[]
    with codecs.open('mainsite/static/files/id3.txt','r','utf-8') as f:
#with open('lensess.txt') as f:
        for line in f.readlines():
        
            line=line.strip()
        
        #line=unicode(line,"utf8")
        #line=line.decode('ascii')
        #line=line.encode("utf-8")
        
            line=line.split('\t')
        
            lense.append(line)
        



    ll=[u'年龄',u'舌苔',u'是否有汗',u'是否畏寒']
    lt=decTree.createTree(lense,ll)
    lt=str(lt).replace('u\'','\'')
    lt=lt.decode("unicode-escape")
    context={'lt':lt}
    #context={'apdieDataSet':apdieDataSet[0]}
    return render(request,'mainsite/id3res.html',context)

@login_required
def knnup(request):
    return render(request,'mainsite/knnup.html')

@login_required
def knnupres(request):
    if request.method == 'POST':
        
        '''knnfile = request.FILES.get('knnfile', None)
        print knnfile
        wb = open( knnfile.name, 'wb+')
        print wb'''
        
        #for chunk in knnfile.chunks():
        #    wb.write(chunk)
        #f=open(request.FILES['knnfile'], None)
        #wb = open(filename='knnfile.txt', file_contents=request.FILES['knnfile'])#.read().replace('\r', ''),'wb'
        #wb=wb.replace('\n', '')
        #f=xlrd.open_workbook(filename=None, file_contents=request.FILES['knnfile'].read())
        x=open('x.txt','wb+')
        wb=request.FILES['knnfile']
        for chunk in wb.chunks():
            x.write(chunk)
        
        #f=f.write(wb)
        #f=request.FILES['knnfile'].read()
        #wb=wb.write(copy.deepcopy(f))
        #f=xlrd.open_workbook(filename=None, file_contents=request.FILES['knnfile'].read())
       # wb=copy.deepcopy(f.read())
        #wb=f.sheets()[0]
        #print wb,x
        #return HttpResponse('ok')
        errorCount,ds,erropercentage=knnUpClassTest('x.txt')
        context={'erropercentage':erropercentage,'ds':ds}
        
        return render(request,'mainsite/knnupres.html',context)
    else:
        return render(request, 'mainsite/knnup.html')
