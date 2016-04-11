from django.conf.urls import patterns, include, url

from .views import attendance

urlpatterns = patterns('',
  url(r'^(?P<event_type>.+?)/(?P<event_id>.+?)/(?P<attendance_hash>.+?)/$', attendance, name='attendance'),
)
