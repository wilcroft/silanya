from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^addch/$', views.addch, name='addch'),
    url(r'^character/(?P<pk>[a-z,A-Z,0-9]+)/$', views.CharacterView.as_view(), name = 'char_view'),
    url(r'^character/(?P<pk>[a-z,A-Z,0-9]+)/edit$', views.editch, name = 'editch'),
    url(r'^addex/$', views.addex, name='addex'),
    url(r'^expedition/(?P<pk>[a-z,A-Z,0-9]+)/$', views.ExpeditionView.as_view(), name = 'ex_view'),
    url(r'^expedition/(?P<pk>[a-z,A-Z,0-9]+)/edit$', views.editex, name = 'editex'),
]
