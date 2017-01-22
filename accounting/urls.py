from django.conf.urls import patterns, include, url

#from .views import index, invoice, payment
from .views import list, payment, invoice, credit

urlpatterns = patterns('',
  url(r'^$', list, name='list'),

  url(r'^payment/(?P<member_id>.+?)/(?P<year>.+?)/$', payment, name='payment'),
  url(r'^credit/(?P<member>.+?)/(?P<year>.+?)/$', credit, name='credit'),
  url(r'^invoice/(?P<member>.+?)/(?P<year>.+?)/$', invoice, name='invoice'),

)
