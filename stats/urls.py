from django.conf.urls import url

from . import views

app_name = 'stats'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[a-z,A-Z,0-9]+)/$', views.CharacterView.as_view(), name = 'char_view')
]
