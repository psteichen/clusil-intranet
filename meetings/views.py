#
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.utils import timezone

from django_tables2  import RequestConfig

from cms.functions import notify_by_email, show_form, visualiseDateTime, genIcal

from events.models import Event
from members.models import Member
from members.functions import get_active_members, gen_fullname, get_member_from_username
from members.groups.models import Group
from members.groups.functions import get_group_members
from attendance.functions import gen_attendance_hashes, gen_invitation_message
from attendance.models import Meeting_Attendance

from .functions import gen_meeting_overview, gen_meeting_initial, gen_current_attendance, gen_report_message
from .models import Meeting, Invitation
from .forms import  MeetingForm, ListMeetingsForm, MeetingReportForm
from .tables  import MeetingTable, MgmtMeetingTable, MeetingMixin, MeetingListingTable


#################
# MEETING VIEWS #
#################

# list #
########
@permission_required('cms.MEMBER',raise_exception=True)
def list(r):
  r.breadcrumbs( ( 
			('board','/board/'),
                   	('meetings','/meetings/'),
               ) )

  table = MeetingTable(Meeting.objects.filter(group__type=Group.WG).order_by('-when'))
  if r.user.has_perm('cms.BOARD'):
    table = MgmtMeetingTable(Meeting.objects.all().order_by('-when'))

  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['template'], {
                   'title': settings.TEMPLATE_CONTENT['meetings']['title'],
                   'desc': settings.TEMPLATE_CONTENT['meetings']['desc'],
                   'actions': settings.TEMPLATE_CONTENT['meetings']['actions'],
                   'table': table,
                })


# add #
#######
@permission_required('cms.BOARD',raise_exception=True)
def add(r):
  r.breadcrumbs( ( 	
			('board','/board/'),
                   	('meetings','/meetings/'),
                   	('add meeting','/meetings/add/'),
               ) )

  if r.POST:
    done_message = ''

    mf = MeetingForm(r.POST,r.FILES)
    if mf.is_valid():
      Mt = mf.save(commit=False)
      Mt.save()
      
      user_member = get_member_from_username(r.user.username)

      if r.FILES:
        I = Invitation(meeting=Mt,message=mf.cleaned_data['additional_message'],attachement=r.FILES['attachement'])
      else:
        I = Invitation(meeting=Mt,message=mf.cleaned_data['additional_message'])
      I.save()

      # all fine -> done
      I.save()
      return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['meetings']['add']['done']['message'] % { 'email': I.message, 'attachement': I.attachement, 'list': ' ; '.join([gen_fullname(a.user) for a in get_group_members(Mt.group)]), },
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MeetingForm()
    return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['meetings']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['add']['submit'],
                'form': form,
                })


# send #
########
@permission_required('cms.BOARD',raise_exception=True)
def send(r, meeting_id):
  r.breadcrumbs( ( 
			('board','/board/'),
                   	('meetings','/meetings/'),
                   	('send meeting invitations','/meetings/send/'),
               ) )

  e_template =  settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['template']

  Mt = Meeting.objects.get(id=meeting_id)
  I = Invitation.objects.get(meeting=Mt)

  title = settings.TEMPLATE_CONTENT['meetings']['send']['done']['title'] % unicode(Mt.group)
  subject = settings.TEMPLATE_CONTENT['meetings']['send']['done']['email']['subject'] % { 'title': unicode(Mt.title) }

  email_error = { 'ok': True, 'who': [], }
  for a in get_group_members(Mt.group):
    u = a.user
   
    gen_attendance_hashes(Mt,Event.MEET,u)
    invitation_message = gen_invitation_message(e_template,Mt,Event.MEET,u) + I.message

    message_content = {
          'FULLNAME'    : gen_fullname(u),
          'MESSAGE'     : invitation_message,
    }
       
    #generate ical invite
    invite = genIcal(Mt)

    #send email
    if I.attachement:
      ok=notify_by_email(u.email,e_subject,message_content,False,[invite,settings.MEDIA_ROOT + unicode(I.attachement)])
    else:
      ok=notify_by_email(u.email,e_subject,message_content,False,invite)
    if not ok:
      email_error['ok']=False
      email_error['who'].append(u.email)

  # error in email -> show error messages
  if not email_error['ok']:
    return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['done']['template'], {
                	'title': title, 
       	        	'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                  })

  # all fine -> done
  else:
    I.sent = timezone.now()
    I.save()
    return render(r, settings.TEMPLATE_CONTENT['meetings']['send']['done']['template'], {
	                'title': title, 
                	'message': settings.TEMPLATE_CONTENT['meetings']['send']['done']['message'] + ' ; '.join([gen_fullname(a.user) for a in get_group_members(Mt.group)]),
                  })


# details #
############
@login_required
def details(r, meeting_id):
  meeting = Meeting.objects.get(id=meeting_id)
  meeting_date = visualiseDateTime(meeting.when)

  r.breadcrumbs( ( 
			('board','/board/'),
                   	('meetings','/meetings/'),
                   	('details for meeting: '+meeting.title + ' ('+ meeting_date+ ')','/meetings/list/'+meeting_id+'/'),
               ) )

  title = settings.TEMPLATE_CONTENT['meetings']['details']['title'] % { 'meeting' : meeting.group, 'date': meeting_date, }
  message = gen_meeting_overview(settings.TEMPLATE_CONTENT['meetings']['details']['overview']['template'],meeting)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['details']['template'], {
                   'title': title,
                   'message': message,
                })


# modify #
##########

#modify helper functions
def show_attendance_form(wizard):
  return show_form(wizard,'meeting','attendance',True)

#modify formwizard
class ModifyMeetingWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyMeetingWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( (
				('board','/board/'),
                                ('meetings','/meetings/'),
                                ('modify a meeting','/meetings/modify/'),
                            ) )

    if self.steps.current != None:
      title = u'réunion'
      meeting_id = self.kwargs['meeting_id']
      title = Meeting.objects.get(pk=meeting_id).title
      context.update({'title': settings.TEMPLATE_CONTENT['meetings']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['meetings']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['meetings']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['meetings']['modify'][self.steps.current]['title'] % { 'meeting': title, } })
      context.update({'next': settings.TEMPLATE_CONTENT['meetings']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyMeetingWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    meeting_id = self.kwargs['meeting_id']
    M = Meeting.objects.get(pk=meeting_id)

    if step == 'meeting':
      form.initial = gen_meeting_initial(M)
      form.instance = M

    if step == 'attendance':
      form.initial = gen_current_attendance(M)

    return form

  def done(self, form_list, form_dict, **kwargs):
    self.request.breadcrumbs( (
				('board','/board/'),
                                ('meetings','/meetings/'),
                                ('modify a meeting','/meetings/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['template']

    M = None
    mf = form_dict['meeting']
    if mf.is_valid():
      M = mf.save()

    title = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['title'] % M

    return render(self.request, template, {
                        'title': title,
                 })


# report #
##########
@permission_required('cms.BOARD',raise_exception=True)
def report(r, meeting_id):
  r.breadcrumbs( ( 	
			('board','/board/'),
                   	('meetings','/meetings/'),
               ) )

  Mt = Meeting.objects.get(id=meeting_id)

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['report']['done']['email']['template']

    mrf = MeetingReportForm(r.POST, r.FILES)
    if mrf.is_valid():
      Mt.report = mrf.cleaned_data['report']
      Mt.save()

      send = mrf.cleaned_data['send']
      if send:
        email_error = { 'ok': True, 'who': [], }
        for m in get_active_members():
   
          #notifiation per email for new report
          subject = settings.TEMPLATE_CONTENT['meetings']['report']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
          message_content = {
            'FULLNAME'    : gen_member_fullname(m),
            'MESSAGE'     : gen_report_message(e_template,Mt,m),
          }
          attachement = settings.MEDIA_ROOT + unicode(Mt.report)
          #send email
          ok=notify_by_email(m.email,subject,message_content,False,attachement)
          if not ok: 
            email_error['ok']=False
            email_error['who'].append(m.email)

        # error in email -> show error messages
        if not email_error['ok']:
          return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                })
        else:
          # done -> with sending
          return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
				'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title_send'], 
                		'message': settings.TEMPLATE_CONTENT['meetings']['report']['done']['message_send'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                })
      else:
        # done -> no sending
        return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
			'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title'], 
                	'message': settings.TEMPLATE_CONTENT['meetings']['report']['done']['message'],
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['report']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mrf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MeetingReportForm(initial={ 'id': Mt.id, 'title': Mt.title, 'when': visualiseDateTime(Mt.when), })
    title = settings.TEMPLATE_CONTENT['meetings']['report']['title'].format(unicode(Mt.group) + ' - ' + unicode(Mt.title))
    return render(r, settings.TEMPLATE_CONTENT['meetings']['report']['template'], {
                'title': title,
                'desc': settings.TEMPLATE_CONTENT['meetings']['report']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['report']['submit'],
                'form': form,
                })



