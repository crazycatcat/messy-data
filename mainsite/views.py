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
    for i in data.split(','):
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

