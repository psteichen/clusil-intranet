from django.conf.urls import patterns, include, url

#from .views import index, invoice, payment
from .views import list, payment

urlpatterns = patterns('',
  url(r'^$', list, name='list'),

#  url(r'^invoice/$', invoice, name='invoice'),
  url(r'^payment/$', payment, name='payment'),

)
