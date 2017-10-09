from django import forms
from .models import Item,itemEntry

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
