from django.conf.urls import url

from .views import submit_idea

urlpatterns = [
  url(r'^$', submit_idea, name='submit_idea'),
]
