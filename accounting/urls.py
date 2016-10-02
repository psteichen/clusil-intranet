from django.conf.urls import patterns, include, url

#from .views import index, invoice, payment
from .views import list, payment, invoice

urlpatterns = patterns('',
  url(r'^$', list, name='list'),

  url(r'^payment/(?P<member_id>.+?)/$', payment, name='payment'),
#  url(r'^credit/(?P<invoice>.+?)/$', credit, name='credit'),
  url(r'^invoice/(?P<member>.+?)/$', invoice, name='invoice'),

)
