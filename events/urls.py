from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from attendance.forms import ModifyAttendanceForm

from .forms import ListEventsForm, ModifyEventForm
from .views import ModifyEventWizard, show_attendance_form
from .views import list, add, send, details

# modify event wizard #
#forms
modify_event_forms = [
        ('event'	, ModifyEventForm),
        ('attendance'	, ModifyAttendanceForm),
]
#condition dict
modify_event_condition_dict = {
	'attendance'	: show_attendance_form,
}
#view
modify_event_wizard = ModifyEventWizard.as_view(modify_event_forms, condition_dict=modify_event_condition_dict)
#wrapper with specific permissions
modify_event_wrapper = permission_required('cms.COMM',raise_exception=True)(modify_event_wizard)

urlpatterns = patterns('',
  url(r'^$', list, name='list'),
  url(r'^list/(?P<event_id>.+?)/$', details, name='details'),

  url(r'^add/$', add, name='add'),
  url(r'^send/(?P<event_id>.+?)/$', send, name='send'),

  url(r'^modify/(?P<event_id>.+?)/$', modify_event_wrapper, name='modify'),
)
