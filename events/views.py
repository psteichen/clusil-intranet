
# coding=utf-8
#
from datetime import date, timedelta, datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from cms.functions import notify_by_email

from members.models import Member
from members.functions import get_active_members, gen_member_fullname
from attendance.functions import gen_invitation_message, gen_hash

from .functions import gen_event_overview, gen_event_initial
from .models import Event, Invitation
from .forms import EventForm, ListEventsForm
from .tables  import EventTable


################
# EVENTS VIEWS #
################

# list #
########
@login_required
def list(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('events','/events/'),
               ) )

  table = EventTable(Event.objects.all().order_by('-id'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['events']['template'], {
                   'title': settings.TEMPLATE_CONTENT['events']['title'],
                   'actions': settings.TEMPLATE_CONTENT['events']['actions'],
                   'table': table,
                })



# add #
#######
@permission_required('cms.COMM',raise_exception=True)
def add(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('events','/events/'),
                   	('add event','/events/add/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['events']['add']['done']['email']['template']

    ef = EventForm(r.POST)
    if ef.is_valid():
      Ev = ef.save(commit=False)
      Ev.save()
      
      I = Invitation(event=Ev,message=ef.cleaned_data['additional_message'])

      send = ef.cleaned_data['send']
      if send:
        email_error = { 'ok': True, 'who': (), }
        for m in get_active_members():
   
          #invitation email with "YES/NO button"
          subject = settings.TEMPLATE_CONTENT['events']['add']['done']['email']['subject'] % { 'title': unicode(Ev.title) }
          invitation_message = gen_invitation_message(e_template,Ev,Event.OTH,m) + ef.cleaned_data['additional_message']
          message_content = {
            'FULLNAME'    : gen_member_fullname(m),
            'MESSAGE'     : invitation_message,
          }
          #send email
          ok=notify_by_email(r.user.email,m.email,subject,message_content)
          if not ok: 
            email_error['ok']=False
            email_error['who'].add(m.email)

        # error in email -> show error messages
        if not email_error['ok']:
          I.sent = datetime.now()
          I.save()
          return render(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                })

      # all fine -> done
      invitation_message = gen_invitation_message(e_template,Ev,Event.OTH,Member(user=r.user)) + ef.cleaned_data['additional_message']
      return render(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['events']['add']['done']['message'] % { 'email': invitation_message, 'list': ' ; '.join([gen_member_fullname(m) for m in get_active_members()]), },
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['events']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in ef.errors]),
                })
  # no post yet -> empty form
  else:
    form = EventForm()
    return render(r, settings.TEMPLATE_CONTENT['events']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['events']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['events']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['events']['add']['submit'],
                'form': form,
                })


# send #
########
@permission_required('cms.COMM',raise_exception=True)
def send(r,event_id):
  r.breadcrumbs( ( 
			('home','/'),
                   	('events','/events/'),
                   	('send event invitations','/events/send/'),
               ) )

  e_template =  settings.TEMPLATE_CONTENT['events']['send']['done']['email']['template']

  Ev = Event.objects.get(id=event_id)
  I = Invitation.objects.get(event=Ev)

  title = settings.TEMPLATE_CONTENT['events']['send']['done']['title'] % unicode(Ev.title)
      
  email_error = { 'ok': True, 'who': (), }
  for m in get_active_members():
   
    #invitation email with "YES/NO button"
    subject = settings.TEMPLATE_CONTENT['events']['send']['done']['email']['subject'] % { 'title': unicode(Ev.title) }
    invitation_message = gen_invitation_message(e_template,Ev,Event.OTH,m)
    message_content = {
      'FULLNAME'    : gen_member_fullname(m),
      'MESSAGE'     : invitation_message,
    }
    #send email
    ok=notify_by_email(r.user.email,m.email,subject,message_content)
    if not ok: 
      email_error['ok']=False
      email_error['who'].add(m.email)

  # error in email -> show error messages
  if not email_error['ok']:
    return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                  })

  # all fine -> done
  else:
    return render(r, settings.TEMPLATE_CONTENT['events']['send']['done']['template'], {
	                'title': title, 
        	        'message': settings.TEMPLATE_CONTENT['events']['send']['done']['message'] + ' ; '.join([gen_member_fullname(m) for m in get_active_members()]),
                  })
 

# details #
###########
@login_required
def details(r, event_id):
  r.breadcrumbs( ( 
			('home','/'),
                   	('events','/events/'),
                   	('details for event n. '+event_id,'/events/details/'+event_id+'/'),
               ) )

  event = Event.objects.get(pk=event_id)
  title = settings.TEMPLATE_CONTENT['events']['details']['title'] % { 'event' : event.title, }
  message = gen_event_overview(settings.TEMPLATE_CONTENT['events']['details']['overview']['template'],event)

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

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyEventWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
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
    self.request.breadcrumbs( ( ('home','/'),
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


