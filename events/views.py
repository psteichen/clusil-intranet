
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils import timezone

from formtools.wizard.views import SessionWizardView
from django_tables2  import RequestConfig

from cms.functions import notify_by_email, group_required

from members.models import Member
from members.functions import get_active_members, gen_fullname, get_member_from_username

from .functions import gen_event_overview, gen_event_initial, gen_reg_hash, gen_reg_code, gen_registration_message
from .models import Event, Invitation, Participant
from .forms import EventForm, ListEventsForm, RegistrationForm
from .tables  import EventTable


################
# EVENTS VIEWS #
################

# list #
########
@group_required('BOARD')
def list(r):
  r.breadcrumbs( ( 
			('board','/board/'),
                   	('events','/events/'),
               ) )

  table = EventTable(Event.objects.all().order_by('-id'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['events']['template'], {
                   'title': settings.TEMPLATE_CONTENT['events']['title'],
                   'actions': settings.TEMPLATE_CONTENT['events']['actions'],
                   'table': table,
                })



# create #
##########

#create helper functions
def show_attendance_form(wizard):
  return show_form(wizard,'meeting','attendance',True)

# create formwizard #
class CreateEventWizard(SessionWizardView):
  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(CreateEventWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( 
				('board','/board/'),
                                ('events','/events/'),
                                ('create an event','/events/create/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['events']['create']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['events']['create']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['events']['create']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['events']['create'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['events']['create'][self.steps.current]['next']})

    return context

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( (
				('board','/board/'),
                                ('events','/events/'),
                                ('create an event','/events/create/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['events']['create']['done']['template']

    E = D = None
    ef = fl[0]
    if ef.is_valid():
      E = ef.save(commit=False)
      E.registration=gen_reg_hash(E)
      E.save()

      I = Invitation(event=E,message=ef.cleaned_data['message'])
      I.save()

    df = fl[1]
    if df.is_valid():
      D = df.save(commit=False)
      D.event = E
      D.save()

    title = settings.TEMPLATE_CONTENT['events']['create']['done']['title'] % E

    return render(self.request, template, {
                        'title'		: title,
#                	'message'	: settings.TEMPLATE_CONTENT['events']['create']['done']['message'] % { 'email': I, 'list': e_list, },
                 })


# send #
########
def send_invitation(event,user,invitation):
  #invitation email with registration link
  subject = settings.TEMPLATE_CONTENT['events']['email']['subject'] % { 'title': unicode(event.title) }
  message_content = {
    'FULLNAME'    : gen_fullname(user),
    'MESSAGE'     : unicode(invitation.message),
  }
  #send email
  try:
    return notify_by_email(user.email,subject,message_content,False,settings.MEDIA_ROOT + unicode(invitation.attachement))
  except:
    return notify_by_email(user.email,subject,message_content)


@group_required('BOARD')
def send(r,event_id):
  r.breadcrumbs( ( 
			('board','/board/'),
                   	('events','/events/'),
                   	('send event invitations','/events/send/'),
               ) )

  Ev = Event.objects.get(id=event_id)
  I = Invitation.objects.get(event=Ev)
      
  email_error = { 'ok': True, 'who': (), }
  recipient_list = []
  for m in get_active_members():
    if m.type == Member.ORG:
      for u in m.users.all():
        recipient_list.append(u.email)
        ok=send_invitation(Ev,u,I)
        if not ok: 
          email_error['ok']=False
          email_error['who'].add(u.email)
    else:
      recipient_list.append(m.head_of_list.email)
      ok=send_invitation(Ev,m.head_of_list,I)
      if not ok: 
        email_error['ok']=False
        email_error['who'].add(m.head_of_list.email)

    # error in email -> show error messages
    if not email_error['ok']:
      I.save()
      return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['send']['done']['title'] % { 'event': Ev.title, }, 
                	'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                  })

  # all fine -> done
  return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
                	'title': settings.TEMPLATE_CONTENT['events']['send']['done']['title'] % { 'event': Ev.title, }, 
                	'message': settings.TEMPLATE_CONTENT['events']['send']['done']['message'] % { 'email': I.message, 'attachement': I.attachement, 'list': ' ; '.join([e for e in recipient_list]), },
              })


# register #
############
def register(r, event_hash):

  E = Event.objects.get(registration=event_hash)

  title 	= settings.TEMPLATE_CONTENT['events']['register']['title'].format(E.title)
  header 	= settings.TEMPLATE_CONTENT['events']['register']['header']
  submit 	= settings.TEMPLATE_CONTENT['events']['register']['submit']

  e_subject 	= settings.TEMPLATE_CONTENT['events']['register']['email']['subject']
  e_template 	= settings.TEMPLATE_CONTENT['events']['register']['email']['template']

  done_title 	= settings.TEMPLATE_CONTENT['events']['register']['done']['title'].format(E.title)

  if r.POST:
    rf = RegistrationForm(r.POST)
    if rf.is_valid():
      P = rf.save(commit=False)
      P.event = E
      P.regcode = gen_reg_code(E,P)
      try:
        P.save()
      except IntegrityError:
        #error duplicate registration
        return render(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
			'title'		: title,
			'error_message'	: settings.TEMPLATE_CONTENT['error']['duplicate'],
		     })

      
      e_message = gen_registration_message(e_template,E,P)

      #notify by email
      message_content = {
        'FULLNAME'    : P.first_name + ' ' + P.last_name.upper(),
        'MESSAGE'     : e_message,
      }
      #send email
      ok=notify_by_email(P.email,e_subject,message_content,False)
      if not ok:
        #error in sending email
        return render(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
			'title'		: title,
			'error_message'	: settings.TEMPLATE_CONTENT['error']['email'],
		     })

      #all fine done page
      done_message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['register']['done']['overview'],E,P)
      return render(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
			'title'		: done_title,
			'message'	: done_message,
		   })
    #error in form
    return render(r, settings.TEMPLATE_CONTENT['events']['register']['done']['template'], {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
		   })



  else: #empty form
    form = RegistrationForm()
    teaser_message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['register']['teaser'],E)
    return render(r, settings.TEMPLATE_CONTENT['events']['register']['template'], {
			'title'		: title,
			'header'	: header,
			'form'		: form,
			'teaser'	: teaser_message,
			'submit'	: submit,
                })




# details #
###########
@group_required('MEMBER')
def details(r, event_id):
  r.breadcrumbs( ( 
			('board','/board/'),
                   	('events','/events/'),
                   	('details for event n. '+event_id,'/events/details/'+event_id+'/'),
               ) )

  event = Event.objects.get(pk=event_id)
  title = settings.TEMPLATE_CONTENT['events']['details']['title'] % { 'event' : event.title, }
  message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['details']['overview'],event)

  return render(r, settings.TEMPLATE_CONTENT['events']['details']['template'], {
                   'title': title,
                   'message': message,
                })


# modify  #
###########

#modify helper functions
def show_attendance_form(wizard):
  return show_form(wizard,'meeting','attendance',True)

# modify formwizard #
class ModifyEventWizard(SessionWizardView):
  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyEventWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( 
				('board','/board/'),
                                ('events','/events/'),
                                ('modify an event','/events/modify/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['events']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['events']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['events']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['events']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['events']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyEventWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'event':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        form.initial = gen_event_initial(cleaned_data['events'])
        form.instance = Event.objects.get(pk=cleaned_data['events'].id)

    return form

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( (
				('board','/board/'),
                                ('events','/events/'),
                                ('modify an event','/events/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['events']['modify']['done']['template']

    E = None
    ef = fl[1]
    if ef.is_valid():
      E = ef.save()

    title = settings.TEMPLATE_CONTENT['events']['modify']['done']['title'] % E

    return render(self.request, template, {
                        'title': title,
                 })



