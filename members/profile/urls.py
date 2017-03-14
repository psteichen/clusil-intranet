from django.conf.urls import patterns, include, url

from .views import profile, invoice
from .views import modify, adduser, affiluser, make_head, make_delegate, rmuser, moduser, invoice, new_invoice, renew

urlpatterns = patterns('',
  #info
  url(r'^$', profile, name='profile'),
  url(r'^invoice/$', invoice, name='invoice'),
  url(r'^invoice/new/$', new_invoice, name='new_invoice'),

  #actions
  url(r'^modify/$', modify, name='modify'),
  url(r'^adduser/$', adduser, name='adduser'),

  url(r'^affiluser/(?P<user>.+?)/$', affiluser, name='affiluser'),
  url(r'^make_head/(?P<user>.+?)/$', make_head, name='make_head'),
  url(r'^make_delegate/(?P<user>.+?)/$', make_delegate, name='make_delegate'),
  url(r'^moduser/(?P<user>.+?)/$', moduser, name='moduser'),
  url(r'^rmuser/(?P<user>.+?)/((?P<really>.+?)/)?$', rmuser, name='rmuser'),

  url(r'^renew/(?P<code>.+?)/$', renew, name='renew'),
)
