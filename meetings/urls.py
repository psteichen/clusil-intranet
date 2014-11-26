from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .forms import ListMeetingsForm, ModifyMeetingForm
from .views import ModifyMeetingWizard
from .views import index, add, attendance, list_all, list
from .views import location_add
from .forms import ListLocationsForm, LocationForm
from .views import ModifyLocationWizard

# modify meeting wizard #
#forms
modify_meeting_forms = [
        ('list'         , ListMeetingsForm),
        ('meeting'	, ModifyMeetingForm),
]
#view
modify_meeting_wizard = ModifyMeetingWizard.as_view(modify_meeting_forms)
#wrapper with specific permissions
modify_meeting_wrapper = login_required(modify_meeting_wizard)

# modify location wizard #
#forms
modify_location_forms = [
        ('list'         , ListLocationsForm),
        ('location'	, LocationForm),
]
#view
modify_location_wizard = ModifyLocationWizard.as_view(modify_location_forms)
#wrapper with specific permissions
modify_location_wrapper = login_required(modify_location_wizard)


urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/$', add, name='add'),
  url(r'^modify/$', modify_meeting_wrapper, name='modify'),
  url(r'^list_all/$', list_all, name='list_all'),
  url(r'^list/(?P<meeting_num>.+?)/$', list, name='list'),

  url(r'^location/add/$', location_add, name='location_add'),
  url(r'^location/modify/$', modify_location_wrapper, name='location_modify'),

  url(r'^attendance/(?P<meeting_num>.+?)/(?P<attendance_hash>.+?)/$', attendance, name='attendance'),
)
