from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Character, Expedition, Player, XP

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

class IndexView(generic.ListView):
    template_name = 'stats/index.html'
    context_object_name = 'character_overview'
        
    def get_queryset(self):
        return Character.objects.order_by('name')

# Create your views here.
