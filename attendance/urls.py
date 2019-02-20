from django.conf.urls import include, url

from .views import attendance, attendance_fast

urlpatterns = [
#  url(r'^(?P<event_type>.+?)/(?P<event_id>.+?)/(?P<attendance_hash>.+?)/$', attendance, name='attendance'),
  url(r'^(?P<event_type>.+?)/(?P<event_id>.+?)/(?P<attendance_hash>.+?)/$', attendance_fast, name='attendance'),
]
