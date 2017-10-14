# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainsite:index'))

'''def register(request):
    if request.method!='POST':
	form=UserCreationForm()
    else:
	form=UserCreationForm(data=request.POST)
	if form.is_valid():
            new_user=form.save()
	    authenticated_user=authenticate(username=new_user.username,email=new_user.email,password=request.POST['password1'])
	    login(request,authenticated_user)
	    return HttpResponseRedirect(reverse('mainsite:index'))
	
    context={'form':form}
    return render(request,'users/register.html',context)'''
	
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            authenticated_user=authenticate(username=new_user.username,email=new_user.email,password=request.POST['password1'])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('mainsite:index'))
            

    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})
	
'''user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('pre_user/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message) # 给该用户发送邮件
            user.email_user(subject=subject, message='message',html_message=message) # 给该用户发送邮件
            return redirect('account_activation_sent')
            # return HttpResponse("邮箱已经发送，请前往验证")'''
