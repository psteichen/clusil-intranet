from django.conf.urls import patterns, include, url

from .views import list, affil, add, modify, adduser

urlpatterns = patterns('',
  url(r'^$', list, name='list'),
  url(r'^affil/(?P<group>.+?)/$', affil, name='affil'),

  url(r'^add/', add, name='add'),
  url(r'^modify/(?P<group>.+?)/$', modify, name='modify'),
  url(r'^adduser/(?P<group>.+?)/$', adduser, name='adduser'),
)
