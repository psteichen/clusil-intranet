from django.conf.urls import patterns, include, url

from .views import index, modify, adduser, tiltuser, chg_hol_d, invoice

urlpatterns = patterns('',
  url(r'^$', index, name='index'),
  url(r'^modify/$', modify, name='modify'),
  url(r'^adduser/$', adduser, name='index'),
  url(r'^tiltuser/$', tiltuser, name='index'),
  url(r'^chg_hol_d/$', chg_hol_d, name='index'),
  url(r'^invoice/$', invoice, name='index'),
)
