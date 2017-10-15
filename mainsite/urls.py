#!/usr/bin/env Python
# coding=utf-8

from django.conf.urls import url,include
from . import views



urlpatterns = [
	#homepage
	url(r'^$',views.index,name='index'),
	#Cahrpters
	url(r'^charpters/$',views.charpters,name='charpters'),
	#Items
	url(r'^items/$',views.items,name='items'),
	#certain chapter
	url(r'^charpters/(?P<charpter_id>\d+)/$',views.charpter,name='charpter'),
	#certain item
	url(r'^items/(?P<item_id>\d+)/$',views.item,name='item'),
	#new item
	url(r'^new_item/$',views.new_item,name='new_item'),
	#new item entry
	url(r'^new_itementry/(?P<item_id>\d+)/$',views.new_itementry,name='new_itementry'),
	#edit item entry
	url(r'^edit_itementry/(?P<itementry_id>\d+)/$',views.edit_itementry,name='edit_itementry'),
	#Statistics
	url(r'^statistics/$',views.statistics,name='statistics'),
	#DesStatistics
	url(r'^statistics/desstat/$',views.desstat,name='desstat'),
	#DesStatisticsResult
	url(r'^statistics/desstat/result/$',views.result,name='result'),
	#DesStatisticsResult-boxplot
	url(r'^statistics/desstat/result/boxplot/$',views.boxplot,name='boxplot'),
	#DesStatisticsResult-hist
	url(r'^statistics/desstat/result/hist/$',views.hist,name='hist'),
	#normtest
	url(r'^statistics/normtest/$',views.normtest,name='normtest'),
	#normresult
	url(r'^statistics/normresult/$',views.normresult,name='normresult'),
	#sdtest
	url(r'^statistics/sdtest/$',views.sdtest,name='sdtest'),
	#sdtestresult
	url(r'^statistics/sdtestresult/$',views.sdtestresult,name='sdtestresult'),
	#dttest
	url(r'^statistics/dttest/$',views.dttest,name='dttest'),
	#dttestres
	url(r'^statistics/dttestres/$',views.dttestres,name='dttestres'),
	#pttest
	url(r'^statistics/pttest/$',views.pttest,name='pttest'),
	#pttestres
	url(r'^statistics/pttestres/$',views.pttestres,name='pttestres'),
	#upttest
	url(r'^statistics/upttest/$',views.upttest,name='upttest'),
	#upttestres
	url(r'^statistics/upttestres/$',views.upttestres,name='upttestres'),
	#attest
	url(r'^statistics/attest/$',views.attest,name='attest'),
	#attestres
	url(r'^statistics/attestres/$',views.attestres,name='attestres'),
	#Dataminings
	url(r'^dataminings/$',views.dataminings,name='dataminings'),
	#Datalabs
	url(r'^datalabs/$',views.datalabs,name='datalabs'),
	#kNN
	url(r'^datalabs/knn/$',views.knn,name='knn'),
	#kNNtest
	url(r'^datalabs/knn/knntest$',views.knntest,name='knntest'),
	#kNNtouch
	url(r'^datalabs/knn/knntouch$',views.knntouch,name='knntouch'),
]



