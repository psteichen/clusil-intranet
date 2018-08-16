from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

from cms.functions import group_required

from .forms import ListEventsForm, EventForm, DistributionForm
from .views import CreateEventWizard, ModifyEventWizard
from .views import list, send, details, register

#forms
event_forms = [
        ('event'	, EventForm),
        ('distrib'	, DistributionForm),
]

# create event wizard #
#view
create_event_wizard = CreateEventWizard.as_view(event_forms)
#wrapper with specific permissions
create_event_wrapper = permission_required('cms.SECR',raise_exception=True)(create_event_wizard)

# modify event wizard #
#view
modify_event_wizard = ModifyEventWizard.as_view(event_forms)
#wrapper with specific permissions
#modify_event_wrapper = permission_required('cms.SECR',raise_exception=True)(modify_event_wizard)
modify_event_wrapper = group_required('BOARD')(modify_event_wizard)

urlpatterns = [
  url(r'^reg/(?P<event_hash>.+?)/$', register, name='register'),

  url(r'^$', list, name='list'),
  url(r'^list/(?P<event_id>.+?)/$', details, name='details'),

  url(r'^create/$', create_event_wrapper, name='create'),

  url(r'^modify/(?P<event_id>.+?)/$', modify_event_wrapper, name='modify'),
  url(r'^send/(?P<event_id>.+?)/$', send, name='send'),

]
