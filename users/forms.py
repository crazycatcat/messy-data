# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='请填写您的邮箱地址')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )