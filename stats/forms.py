from django import forms
from django.forms import formset_factory
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminDateWidget
from markdownx.fields import MarkdownxFormField

from .models import Player, Expedition, Character, XP

class chStatusWidget(forms.ChoiceField):
    class Media:
        js = ('disable_dd_date.js')

class XPForm(forms.Form):
    char = forms.ModelChoiceField(queryset=Character.objects.all(), label=mark_safe('<br />Name'))#.filter(status!=Character.DEAD).filter(status!=Character.DEPARTED), label='Name')
    value = forms.IntegerField(label='XP')

class AddExForm(forms.Form):
    name = forms.CharField(label='Expedition Name')
    slug = forms.SlugField(label='Expedition Slug')
    dm = forms.ModelChoiceField(queryset=Player.objects.all(),label='DM')
    date = forms.DateField(label='Expedition Date') 

    log = MarkdownxFormField()

    def __init__(self, *args, **kwargs):
        super(AddExForm,self).__init__(*args, **kwargs)
        
class EditExForm(AddExForm):
    slug = forms.SlugField(label='Expedition Slug', disabled=True)

class AddChForm(forms.Form):
    name = forms.CharField(label='Character Name')
    slug = forms.SlugField(label='Slug')
    player = forms.ModelChoiceField(queryset=Player.objects.order_by('name'),label='Player')

class EditChForm(AddChForm):
    STATUS_CHOICES = (
        ('A', 'Alive'),
        ('D', 'Dead'),
        ('G', 'Departed')
    )
#    alive = forms.BooleanField(label='Alive?')
    #status = chStatusWidget(choices=STATUS_CHOICES, initial='Alive', label='Status')
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='Alive', label='Status', widget=forms.Select(attrs={'onChange':'activateDDField(this)'}))
    dd_date = forms.ModelChoiceField(queryset=Expedition.objects.order_by('-date'),label='Final Expedition', required=False)

class EditAliveChForm(EditChForm):
    dd_date = forms.ModelChoiceField(queryset=Expedition.objects.order_by('-date'),label='Final Expedition', required=False, disabled=True)

class EditDDChForm(EditChForm):
    dd_date = forms.ModelChoiceField(queryset=Expedition.objects.order_by('-date'),label='Final Expedition', required=True, disabled=False)

class CarryXPForm(forms.Form):
    TYPE_CHOICE = (
        ('P', 'Pool'),
        ('L', 'Lump-Sum')
    )
    value = forms.IntegerField(label='XP')
    ex = forms.ModelChoiceField(queryset=Expedition.objects.order_by('-date'), label="After Expedition")
    carrytype = forms.ChoiceField(choices=TYPE_CHOICE, label='Type', initial='Pool')
