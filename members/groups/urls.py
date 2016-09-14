from django.conf.urls import patterns, include, url

from .views import list, affil, add, modify

urlpatterns = patterns('',
  url(r'^$', list, name='list'),
  url(r'^affil/(?P<group>.+?)/$', affil, name='affil'),

  url(r'^add/', add, name='add'),
  url(r'^modify/(?P<group>.+?)/$', modify, name='modify'),
)
