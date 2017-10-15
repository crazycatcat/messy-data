#!/usr/bin/env Python
# coding=utf-8
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Charpter,Item,itemEntry,Statistic,DataMining,DataLab

from django.http import HttpResponseRedirect,Http404,HttpResponse

from django.core.urlresolvers import reverse

from .forms import ItemForm,itemEntryForm

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

from scipy.stats import kstest,levene,ttest_1samp,ttest_rel,ttest_ind
from .knn import *



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
    requestData=request.GET.copy()
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