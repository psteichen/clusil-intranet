from django.conf.urls import include, url

from .views import attendance

urlpatterns = [
  url(r'^(?P<event_type>.+?)/(?P<event_id>.+?)/(?P<attendance_hash>.+?)/$', attendance, name='attendance'),
]
