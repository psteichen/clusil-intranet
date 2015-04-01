#
# coding=utf-8
#
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from intranet.functions import notify_by_email

from members.functions import get_active_members, gen_fullname

from .functions import gen_invitation_message, gen_hash, gen_meeting_overview, gen_meeting_initial, gen_location_initial
from .models import Location, Meeting
from .forms import LocationForm, MeetingForm
from .tables  import MeetingTable


# index #
#########
@login_required
def index(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
               ) )

  return render(r, settings.TEMPLATE_CONTENT['meetings']['template'], {
                   'title': settings.TEMPLATE_CONTENT['meetings']['title'],
                   'actions': settings.TEMPLATE_CONTENT['meetings']['actions'],
               })


##################
# LOCATION VIEWS #
##################

# location_add #
################
@login_required
def location_add(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('add a location','/meetings/location/add/'),
               ) )

  if r.POST:
    lf = LocationForm(r.POST)
    if lf.is_valid():
      Lo = lf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['meetings']['location']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['location']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['meetings']['location']['add']['done']['message'] + unicode(Lo),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['meetings']['location']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['location']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in lf.errors]),
                })

  # no post yet -> empty form
  else:
    form = LocationForm()
    return render(r, settings.TEMPLATE_CONTENT['meetings']['location']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['location']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['meetings']['location']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['location']['add']['submit'],
                'form': form,
                })

# modify_location formwizard #
##############################
class ModifyLocationWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyLocationWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('modify a location','/meetings/location/modify/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['meetings']['location']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['meetings']['location']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['meetings']['location']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['meetings']['location']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['meetings']['location']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyLocationWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'location':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        form.initial = gen_location_initial(cleaned_data['locations'])
        form.instance = Location.objects.get(pk=cleaned_data['locations'].id)

    return form

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('modify a location','/meetings/location/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['meetings']['location']['modify']['done']['template']

    L = None
    lf = fl[1]
    if lf.is_valid():
      L = lf.save()

    title = settings.TEMPLATE_CONTENT['meetings']['location']['modify']['done']['title'] % L

    return render(self.request, template, {
                        'title': title,
                 })


#################
# MEETING VIEWS #
#################

# add #
#######
@login_required
def add(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('add a meeting','/meetings/add/'),
               ) )

  if r.POST:
    e_template =  settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['template']

    mf = MeetingForm(r.POST)
    if mf.is_valid():
      Mt = mf.save(commit=False)
      Mt.save()
      
      email_error = { 'ok': True, 'who': (), }
      for m in get_active_members():
   
        #invitation email with "YES/NO button"
#        subject = settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['subject'].format(title=unicode(Mt.title)))
        subject = settings.TEMPLATE_CONTENT['meetings']['add']['done']['email']['subject'] % { 'title': unicode(Mt.title) }
        invitation_message = gen_invitation_message(e_template,Mt,m)
        message_content = {
          'FULLNAME'    : gen_fullname(m),
          'MESSAGE'     : invitation_message + mf.cleaned_data['additional_message'],
        }
        #send email
        ok=notify_by_email(r.user.email,m.email,subject,message_content)
        if not ok: 
          email_error['ok']=False
          email_error['who'].add(m.email)

      # error in email -> show error messages
      if not email_error['ok']:
        return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['email'] + ' ; '.join([e for e in email_error['who']]),
                })

      # all fine -> done
      else:
        return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['meetings']['add']['done']['message'] + ' ; '.join([gen_fullname(m) for m in get_active_members()]),
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
    try:
      latest = Meeting.objects.values().latest('num')
      next_num = latest['num'] + 1
      form = MeetingForm(initial={ 'title': str(next_num) + '. réunion statutaire', 'num': next_num, })
    except Meeting.DoesNotExist:
      pass
    return render(r, settings.TEMPLATE_CONTENT['meetings']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['meetings']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['meetings']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['meetings']['add']['submit'],
                'form': form,
                })

# list #
#########
@login_required
def list(r, meeting_num):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('list meeting n. '+meeting_num,'/meetings/list/'+meeting_num+'/'),
               ) )

  meeting = Meeting.objects.get(num=meeting_num)
  title = settings.TEMPLATE_CONTENT['meetings']['list']['title'] % { 'num' : meeting_num, }
  message = gen_meeting_overview(settings.TEMPLATE_CONTENT['meetings']['list']['overview']['template'],meeting)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['list']['template'], {
                   'title': title,
                   'message': message,
                })

# list_all #
#########
@login_required
def list_all(r):
  r.breadcrumbs( ( ('home','/'),
                   ('meetings','/meetings/'),
                   ('list meetings','/meetings/list_all/'),
               ) )

  table = MeetingTable(Meeting.objects.all().order_by('-num'))
  RequestConfig(r, paginate={"per_page": 75}).configure(table)

  return render(r, settings.TEMPLATE_CONTENT['meetings']['list_all']['template'], {
                   'title': settings.TEMPLATE_CONTENT['meetings']['list_all']['title'],
                   'desc': settings.TEMPLATE_CONTENT['meetings']['list_all']['desc'],
                   'table': table,
                })


# modify formwizard #
#####################
class ModifyMeetingWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyMeetingWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('modify a meeting','/meetings/modify/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['meetings']['modify']['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['meetings']['modify']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['meetings']['modify']['prev']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['meetings']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['meetings']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyMeetingWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'meeting':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        form.initial = gen_meeting_initial(cleaned_data['meetings'])
        form.instance = Meeting.objects.get(pk=cleaned_data['meetings'].id)

    return form

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( ( ('home','/'),
                                ('meetings','/meetings/'),
                                ('modify a meeting','/meetings/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['template']

    M = None
    mf = fl[1]
    if mf.is_valid():
      M = mf.save()

    title = settings.TEMPLATE_CONTENT['meetings']['modify']['done']['title'] % M

    return render(self.request, template, {
                        'title': title,
                 })


#############################
# NONE LOGIN_REQUIRED VIEWS #
#############################

# attendance #
##############
def attendance(r, meeting_num, attendance_hash):
  meeting = Meeting.objects.get(num=meeting_num)

  title = settings.TEMPLATE_CONTENT['meetings']['attendance']['title'] % { 'meeting': meeting.title, }
  message = ''
  notify=False

  for m in get_active_members():
    if gen_hash(meeting,m.email) == attendance_hash:
      # it's a YES
      meeting.attendance.add(m)
      message = settings.TEMPLATE_CONTENT['meetings']['attendance']['yes'] % { 'name': gen_fullname(m), }
      notify=True

    if gen_hash(meeting,m.email,False) == attendance_hash:
      # it's a NO
      meeting.excused.add(m)
      message = settings.TEMPLATE_CONTENT['meetings']['attendance']['no'] % { 'name': gen_fullname(m), }
      notify=True

  if notify:
    #notify by email
    message_content = {
      'MESSAGE'     : message,
    }
    #send email
    ok=notify_by_email(False,m.email,title,message_content)

  meeting.save()

  return render(r, settings.TEMPLATE_CONTENT['meetings']['attendance']['template'], {
                   'title': title,
                   'message': message,
               })

