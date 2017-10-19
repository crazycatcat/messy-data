#!/usr/bin/env Python
# coding=utf-8
from django import forms
from .models import Item,itemEntry

from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

class ItemForm(forms.ModelForm):
    class Meta:
	    model=Item
	    fields=['title']
	    labels={'title':''}


class itemEntryForm(forms.ModelForm):
    class Meta:
	    model=itemEntry
	    fields=['text']
	    labels={'text':''}
	    widgets={'text':forms.Textarea(attrs={'cols':80})}


def validate_excel(value):
    if value.name.split('.')[-1] not in ['xls','xlsx']:
        raise ValidationError(_('Invalid File Type: %(value)s'),params={'value': value},)

class UploadExcelForm(forms.Form):
    excel = forms.FileField(validators=[validate_excel]) #这里使用自定义的验证
