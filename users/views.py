# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainsite:index'))

def register(request):
    if request.method!='POST':
	form=UserCreationForm()
    else:
	form=UserCreationForm(data=request.POST)
	if form.is_valid():
            new_user=form.save()
	    authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
	    login(request,authenticated_user)
	    return HttpResponseRedirect(reverse('mainsite:index'))
	
    context={'form':form}
    return render(request,'users/register.html',context)
