import sys
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.forms import formset_factory

from .models import Character, Expedition, Player, XP
from .forms import AddExForm, XPForm, EditExForm

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

class AddView(generic.CreateView):
    model = Expedition
    fields = ['slug', 'name', 'dm', 'date' ]
#    fields = ['slug', 'name', 'dm', 'date', 'members' ]
    template_name = 'stats/add.html'
    
#    def __init__(self, *arfs, **kwargs):
#        super(AddView
#    def form_valid(self, form):
                

# Create your views here.

def add(request):
    CharFormSet = formset_factory(XPForm, extra=1)
    if request.method == 'POST':
##        print (request.POST['dm'], file=sys.stderr)
        if 'add' in request.POST:
            charformset = CharFormSet(request.POST, prefix='chars')
            form= AddExForm(request.POST)
            print("Adding to form, now at ", charformset.total_form_count(), file=sys.stderr)
        elif 'submit' in request.POST:
            x = Expedition()
            x.dm = Player.objects.get(pk=request.POST['dm'])
            x.name = request.POST['name']
            x.date = request.POST['date']
            x.slug = request.POST['slug']
            
            x.save()
            charformset = CharFormSet(request.POST, prefix='chars')
#            print("Adding to form, now at ", charformset.total_form_count(), file=sys.stderr)
##            print (charformset, file=sys.stderr)
            for c in charformset:
                c.is_valid()
##              print (c.is_valid(), file=sys.stderr)
##              print (c.cleaned_data, file=sys.stderr)
##              print (c.cleaned_data['char'], file=sys.stderr)
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

    return render(request, 'stats/add.html', {'form':form, 'charformset':charformset})

def edit(request, pk):
    CharFormSet = formset_factory(XPForm, extra=1)
    if request.method == 'POST':
        form = AddExForm(request.POST)
        form.is_valid()
        print(form.fields['slug'].initial, file=sys.stderr)
       # print(form.cleaned_data, file=sys.stderr)
        x = Expedition.objects.get(slug=request.POST['slug'])
        x.dm = Player.objects.get(pk=request.POST['dm'])
        x.name = request.POST['name']
        x.members.clear()
        charformset = CharFormSet(request.POST, prefix='chars')
        chars_found = []
#        print("Adding to form, now at ", charformset.total_form_count(), file=sys.stderr)
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
        form = AddExForm(initial={'dm':x.dm, 'name':x.name, 'date':x.date, 'slug':x.slug})
        form['slug'].disabled=True
        CharFormSet= formset_factory(XPForm, extra=0)
        initial_data = []
        for xp in XP.objects.all().filter(expedition=x):
            initial_data.append({'char' : xp.character, 'value' : xp.value,})
        charformset = CharFormSet(prefix='chars', initial=initial_data) 

    return render(request, 'stats/edit.html', {'form':form, 'charformset':charformset})
