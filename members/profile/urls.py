from django.conf.urls import patterns, include, url

from .views import profile, invoice
from .views import modify, adduser, affiluser, rmuser, chg_hol_d, invoice

urlpatterns = patterns('',
  #info
  url(r'^$', profile, name='profile'),
  url(r'^invoice/$', invoice, name='invoice'),

  #actions
  url(r'^modify/$', modify, name='modify'),
  url(r'^adduser/$', adduser, name='adduser'),
  url(r'^affiluser/$', affiluser, name='affiluser'),
  url(r'^rmuser/$', rmuser, name='rmuser'),
  url(r'^chg_hol_d/$', chg_hol_d, name='chg_hol_d'),
)
