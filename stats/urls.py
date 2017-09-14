from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^character/(?P<pk>[a-z,A-Z,0-9]+)/$', views.CharacterView.as_view(), name = 'char_view'),
    url(r'^add/$', views.add, name='add'),
    url(r'^expedition/(?P<pk>[a-z,A-Z,0-9]+)/$', views.ExpeditionView.as_view(), name = 'ex_view'),
    url(r'^expedition/(?P<pk>[a-z,A-Z,0-9]+)/edit$', views.edit, name = 'edit'),
]
