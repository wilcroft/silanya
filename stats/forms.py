from django import forms
from django.forms import formset_factory
from django.utils.safestring import mark_safe

from .models import Player, Expedition, Character, XP

class XPForm(forms.Form):
    char = forms.ModelChoiceField(queryset=Character.objects.all(), label=mark_safe('<br />Name'))#.filter(status!=Character.DEAD).filter(status!=Character.DEPARTED), label='Name')
    value = forms.IntegerField(label='XP')

class AddExForm(forms.Form):
    name = forms.CharField(label='Expedition Name')
    slug = forms.SlugField(label='Expedition Slug')
    dm = forms.ModelChoiceField(queryset=Player.objects.all(),label='DM')
    date = forms.DateField(label='Expedition Date')
#    charset_factory = formset_factory(XPForm)
#    charset = charset_factory()
#    fields['chars'] = []

    def __init__(self, *args, **kwargs):
        super(AddExForm,self).__init__(*args, **kwargs)
#        self.fields['chars'] = [forms.ModelChoiceField(queryset=Character.objects.all().filter(status!=Character.DEAD).filter(status!=Character.DEPARTED), label='Name'), forms.IntegerField(label='XP')]
#        self.kwargs['chars'].append([forms.ModelChoiceField(queryset=Character.objects.all().filter(status!=Character.DEAD).filter(status!=Character.DEPARTED), label='Name'), forms.IntegerField(label='XP')])
        
