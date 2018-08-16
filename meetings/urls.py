from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

from cms.functions import group_required
#from attendance.forms import ModifyAttendanceForm

from .forms import ListMeetingsForm, ModifyMeetingForm, ModifyInvitationForm
from .views import ModifyMeetingWizard, show_invitation_form
from .views import list, add, send, details, report, delete

# modify meeting wizard #
#forms
modify_meeting_forms = [
        ('meeting'	, ModifyMeetingForm),
#        ('attendance'	, ModifyAttendanceForm),
        ('invitation'	, ModifyInvitationForm),
]
#condition dict
modify_meeting_condition_dict = {
#	'attendance'	: show_attendance_form,
	'invitation'	: show_invitation_form,
}
#view
modify_meeting_wizard = ModifyMeetingWizard.as_view(modify_meeting_forms, condition_dict=modify_meeting_condition_dict)
#wrapper with specific permissions
#modify_meeting_wrapper = permission_required('cms.BOARD',raise_exception=True)(modify_meeting_wizard)
modify_meeting_wrapper = group_required('BOARD')(modify_meeting_wizard)

urlpatterns = [
  url(r'^$', list, name='list'),
  url(r'^list/(?P<meeting_id>.+?)/$', details, name='details'),

#below urls need permissions
  url(r'^add/$', add, name='add'),
  url(r'^send/(?P<meeting_id>.+?)/$', send, name='send'),
  url(r'^modify/(?P<meeting_id>.+?)/$', modify_meeting_wrapper, name='modify'),
  url(r'^report/(?P<meeting_id>.+?)/$', report, name='report'),
  url(r'^delete/(?P<meeting_id>.+?)/$', delete, name='delete'),
]
