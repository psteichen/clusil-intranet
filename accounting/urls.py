from django.conf.urls import patterns, include, url

#from .views import index, invoice, payment
from .views import index, payment

urlpatterns = patterns('',
  url(r'^$', index, name='index'),

#  url(r'^invoice/$', invoice, name='invoice'),
  url(r'^payment/$', payment, name='payment'),

)
