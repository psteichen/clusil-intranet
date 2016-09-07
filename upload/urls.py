from django.conf.urls import patterns, include, url

from .views import upload, import_data

urlpatterns = patterns('',
  url(r'^data/(?P<ty>.+?)/$', import_data, name='import_data'),
  url(r'^file/(?P<campaign>.+?)/$', upload, name='upload'),
)
