import sys
import pdb
import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.forms import formset_factory
from markdownx.utils import markdownify
from django.utils.safestring import mark_safe

from .models import Character, Expedition, Player, XP, CXP
from .forms import AddExForm, XPForm, EditChForm, AddChForm, CarryXPForm, EditAliveChForm, EditDDChForm

class CharacterView(generic.ListView):
    template_name = 'stats/charlist.html'
    context_object_name = 'char_ex_list'
    char = Character()

    def get_queryset(self):#, char):
#        charid = Character.objects.get(slug=pk)
#        char = get_object_or_404(Character, slug=self.request)
        self.char = get_object_or_404(Character, slug=self.kwargs['pk'])
        return Expedition.objects.all().filter(members=self.char)
    
    def get_context_data(self, **kwargs):
        context = super(CharacterView, self).get_context_data(**kwargs)
        context['char'] = Character.objects.get(slug=self.kwargs['pk'])
        return context

class ExpeditionView(generic.ListView):
    template_name = 'stats/exlist.html'
    context_object_name = 'ex_list'
    ex = Expedition()

    def get_queryset(self):#, char):
        self.ex = get_object_or_404(Expedition, slug=self.kwargs['pk'])
        return XP.objects.all().filter(expedition=self.ex)
    
    def get_context_data(self, **kwargs):
        context = super(ExpeditionView, self).get_context_data(**kwargs)
        context['ex'] = Expedition.objects.get(slug=self.kwargs['pk'])
        context['log'] = mark_safe(markdownify( Expedition.objects.get(slug=self.kwargs['pk']).log))
        return context

class IndexView(generic.ListView):
    template_name = 'stats/index.html'
    context_object_name = 'character_overview'
        
    def get_queryset(self):
        return Character.objects.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['allex'] = Expedition.objects.order_by('-date')
        return context

# Create your views here.

def addex(request):
    URL='stats/addex.html'
    CharFormSet = formset_factory(XPForm, extra=1)
    if request.method == 'POST':
        form = AddExForm(request.POST) 
        charformset = CharFormSet(request.POST, prefix='chars')
        charlist = []
    #Validate forms
        if form.is_valid()==False:
            return render(request, URL, {'form':form, 'charformset':charformset})
        if charformset.is_valid()==False:
            return render(request, URL, {'form':form, 'charformset':charformset})
        for c in charformset:
            c.is_valid()
            if c.is_valid()==False or c.cleaned_data == {} or c.cleaned_data['char'] is None or c.cleaned_data['value'] is None:
                return render(request, URL, {'form':form, 'charformset':charformset})
            charlist.append(c.cleaned_data['char'])
        if len(charlist) > len(set(charlist)):
            return render(request, URL, {'form':form, 'charformset':charformset})
        if Expedition.objects.filter(slug=request.POST['slug']).exists():
            # We have a dupe slug, send an error notice
            return render(request, URL, {'form':form, 'charformset':charformset})
        elif 'submit' in request.POST:
            #print(charformset, file=sys.stderr)
            x = Expedition()
            x.dm = Player.objects.get(pk=request.POST['dm'])
            x.name = request.POST['name']
            x.date = request.POST['date']
            x.slug = request.POST['slug']
            x.log = form.cleaned_data['log']
            
            x.save()
            for c in charformset:
                c.is_valid()
                x.members.add(Character.objects.get(pk=c.cleaned_data['char'].pk))
                xp = XP()
                xp.expedition = x
                xp.character = Character.objects.get(pk=c.cleaned_data['char'].pk)
                xp.value = c.cleaned_data['value']
                xp.save()
            x.save()
            return HttpResponseRedirect(reverse('stats:index'))
    else: 
        form = AddExForm()
        charformset = CharFormSet(prefix='chars') 

    return render(request, URL, {'form':form, 'charformset':charformset})

def editex(request, pk):
    URL='stats/editex.html'
    CharFormSet = formset_factory(XPForm, extra=1)
    if request.method == 'POST':
        form = AddExForm(request.POST)
        form.is_valid()
        x = Expedition.objects.get(slug=request.POST['slug'])
        x.dm = Player.objects.get(pk=request.POST['dm'])
        x.name = request.POST['name']
        x.date = form.cleaned_data['date']
        x.log = form.cleaned_data['log']
        x.members.clear()
        charformset = CharFormSet(request.POST, prefix='chars')
        chars_found = []
        for c in charformset:
            c.is_valid()
            char = Character.objects.get(pk=c.cleaned_data['char'].pk)
            x.members.add(char)
            chars_found.append(char)
            if XP.objects.filter(expedition=x).filter(character=char).exists():
                xp = XP.objects.get(expedition=x,character=char)
            else:
                xp = XP()
                xp.expedition = x
                xp.character = char
            xp.value = c.cleaned_data['value']
            xp.save()
        oldchars = XP.objects.filter(expedition=x).exclude(character__in=chars_found)
        for oc in oldchars:
            oc.delete()    
        x.save()
        return HttpResponseRedirect(reverse('stats:index'))
    else: 
        x = Expedition.objects.get(slug=pk);
        form = AddExForm(initial={'dm':x.dm, 'name':x.name, 'date':x.date, 'slug':x.slug, 'log':x.log})
        form['slug'].disabled=True
        CharFormSet= formset_factory(XPForm, extra=0)
        initial_data = []
        for xp in XP.objects.all().filter(expedition=x):
            initial_data.append({'char' : xp.character, 'value' : xp.value,})
        charformset = CharFormSet(prefix='chars', initial=initial_data) 

    return render(request, URL, {'form':form, 'charformset':charformset})

def addch(request):
    URL='stats/addch.html'
    if request.method == 'POST':
        form = AddChForm(request.POST)
        if form.is_valid()==False:
            return render(request, URL, {'form':form})
        if Character.objects.filter(slug=form.cleaned_data['slug']).exists():
            return render(request, URL, {'form':form})
        c = Character()
        c.slug=form.cleaned_data['slug']
        c.name=form.cleaned_data['name']
        c.player=Player.objects.get(pk=form.cleaned_data['player'].pk)
        c.save()
        return HttpResponseRedirect(reverse('stats:index'))
    else:
        form = AddChForm()
    return render(request, URL, {'form':form})

def editch(request,pk):
    URL='stats/editch.html'
    CarryFormset = formset_factory(CarryXPForm, extra=0)
    c = Character.objects.get(slug=pk)
    cx_initial = []
    for cx in CXP.objects.filter(character=c):
        porls = 'L' if cx.lumpNotPool else 'P'
        cx_initial.append({'value':cx.value,'ex':cx.expedition,'carrytype':porls})
    
    if request.method == 'POST':
        form = EditChForm(request.POST)
        carryformset = CarryFormset(request.POST, initial=cx_initial, prefix='carry')
    #Validate form
        if form.is_valid()==False:
            return render(request,URL, {'form':form, 'carryformset':carryformset})
        if carryformset.is_valid()==False:
            return render(request, URL, {'form':form, 'carryformset':carryformset})
        for cx in carryformset:
            cx.is_valid()
            if cx.cleaned_data == {} or cx.cleaned_data['value'] is None \
                        or cx.cleaned_data['ex'] is None or cx.cleaned_data['carrytype'] is None:
                return render(request, URL, {'form':form, 'charformset':charformset})
        c.name = form.cleaned_data['name']
        c.player = Player.objects.get(pk=form.cleaned_data['player'].pk)
        if form.cleaned_data['status']=='A': c.status=Character.ACTIVE
        elif form.cleaned_data['status']=='D': 
            c.status=Character.DEAD
            c.dd_date = Expedition.objects.get(pk=form.cleaned_data['dd_date'].pk).date
        elif form.cleaned_data['status']=='G': c.status=Character.DEPARTED
        c.save()
        for cxp in CXP.objects.filter(character=c):
            cxp.delete()
        for cx in carryformset:
            cxp = CXP()
            cxp.character = c
            cxp.expedition = Expedition.objects.get(pk=cx.cleaned_data['ex'].pk)
            cxp.value = cx.cleaned_data['value']
            cxp.lumpNotPool = cx.cleaned_data['carrytype']!='P'
            cxp.save()
            
        return HttpResponseRedirect(reverse('stats:index'))
    else:
        form_initial= { 'slug' : c.slug, 'name' : c.name, 'player' : c.player,}
        if c.status==Character.DEAD: 
            form_initial['status'] = 'D'
            form_initial['dd_date'] = Expedition.objects.get(date=c.dd_date)
            form = EditDDChForm(initial=form_initial)
        elif c.status==Character.DEPARTED: 
            form_initial['status'] = 'G'
            form_initial['dd_date'] = Expedition.objects.get(date=c.dd_date)
            form = EditDDChForm(initial=form_initial)
        else: 
            form_initial['status'] = 'A'
            form = EditAliveChForm(initial=form_initial)
        carryformset = CarryFormset(prefix='carry', initial=cx_initial)
        emptyformset = CarryFormset().empty_form
    return render(request, URL, {'form':form, 'carryformset':carryformset, 'emptyformset':emptyformset})
