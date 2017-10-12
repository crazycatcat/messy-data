#!/usr/bin/env Python
# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Charpter(models.Model):
    title=models.CharField(max_length=200)
    #slug
    #body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    #owner=models.ForeignKey(User)
    
    class Meta:
        ordering=('-pub_date',)
      
    def __unicode__(self):
        return self.title

class charpterEntry(models.Model):
    chapter=models.ForeignKey(Charpter)
    text=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
	
    class Meta:
	verbose_name_plural='charpterentries'
        
      
    def __unicode__(self):
        return self.text[:50]+'...'

		
		
class Item(models.Model):
    title=models.CharField(max_length=200)
    #slug
    #body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    owner=models.ForeignKey(User)
    
    class Meta:
	    ordering=('-pub_date',)
        
      
    def __unicode__(self):
        return self.title
		
class itemEntry(models.Model):
    item=models.ForeignKey(Item)
    text=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
	
    class Meta:
	verbose_name_plural='itementries'
        
      
    def __unicode__(self):
        return self.text[:50]+'...'
		
class Statistic(models.Model):
    title=models.CharField(max_length=200)
    #slug
    #body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    #owner=models.ForeignKey(User)
    
    class Meta:
        ordering=('-pub_date',)
      
    def __unicode__(self):
        return self.title
		
class DataMining(models.Model):
    title=models.CharField(max_length=200)
    #slug
    #body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    #owner=models.ForeignKey(User)
    
    class Meta:
        ordering=('-pub_date',)
      
    def __unicode__(self):
        return self.title

class DataLab(models.Model):
    title=models.CharField(max_length=200)
    #slug
    #body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    #owner=models.ForeignKey(User)
    
    class Meta:
        ordering=('-pub_date',)
      
    def __unicode__(self):
        return self.title


		
'''class StatEntry(models.Model):
    title=models.ForeignKey(Statistic)
    #text=models.TextField()
    #pub_date=models.DateTimeField(default=timezone.now)
	
    class Meta:
	verbose_name_plural='itementries'
        
      
    def __unicode__(self):
        return self.title	

class DesStat(models.Model):
    #title=models.CharField(max_length=200)
    #slug
    body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    #owner=models.ForeignKey(User)
    
    class Meta:
        ordering=('-pub_date',)
      
    def __unicode__(self):
        return self.title'''