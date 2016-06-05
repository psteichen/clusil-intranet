from django.conf.urls import patterns, include, url

from .views import index

urlpatterns = patterns('',
  url(r'(?P<campaign>.+?)/$', index, name='index'),
)
