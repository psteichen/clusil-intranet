from django.conf.urls import patterns, url

from .views import submit_idea

urlpatterns = patterns('',
  url(r'^$', submit_idea, name='submit_idea'),
)
