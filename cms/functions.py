# -*- coding: utf-8 -*-
from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone


###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################
def debug(app,message):
  if settings.DEBUG:
    from sys import stderr as errlog
    print >>errlog, 'DEBUG ['+str(app)+']: '+str(message)

def group_required(group_name):
  from django.contrib.auth.decorators import user_passes_test
  from django.core.exceptions import PermissionDenied

  """Requires user membership in at least one of the groups passed in."""
  def in_group(user):
    if user.is_authenticated():
      if bool(user.groups.filter(name=group_name)) or user.is_superuser:
        return True
      else:
        raise PermissionDenied

  return user_passes_test(in_group)


def attach_to_email(email,attachment):
  from os import path
  from django.core.files.storage import default_storage
  from django.core.files.base import ContentFile

  try: email.attach(attachment)
  except:
    try: email.attach_file(attachment)
    except:
      tmp_file = default_storage.save(path.join(settings.MEDIA_ROOT, 'tmp', attachment.name), ContentFile(attachment.read()))
      email.attach_file(tmp_file)
      tmp_file = default_storage.delete(path.join(settings.MEDIA_ROOT, 'tmp', attachment.name))

def notify_by_email(to,subject,message_content,template='default.txt',attachment=None,copy=None):
  from django.core.mail import EmailMessage
  is_array = lambda var: isinstance(var, (list, tuple))

  if not template: template='default.txt'

  email = EmailMessage(
                subject=subject, 
                from_email=settings.EMAILS['email']['no-reply'], 
                to=[to]
          )
  if copy: email.cc=[settings.EMAILS['email']['secgen']]

  # add default footer (questions, salutation and disclaimer)
  message_content['SALUTATION'] = settings.EMAILS['salutation']
  message_content['DISCLAIMER'] = settings.EMAILS['disclaimer']
  email.body = render_to_string(template,message_content)
  if attachment:
    if is_array(attachment):
      for a in attachment: attach_to_email(email,a)
    else: attach_to_email(email,attachment)

  return email.send()

#  try:
#    email.send()
#    return True
#  except:
#    return False

def show_form(wiz,step,field,const):
  cleaned_data = wiz.get_cleaned_data_for_step(step) or {}
  d = cleaned_data.get(field) or 666
  return int(d) == const

def gen_form_errors(form):
  output='<ul>'
  for f in form:
    for e in f.errors:
      output+='<li><i>'+unicode(f.label)+'</i>:   <b>'+e+'</b></li>'

  output+='</ul>'
  return output

def visualiseDecimal(decIn,currency=''):
  s = '{:,.12g}'.format(decIn)
  s = s.replace(',', ' ')
  s = s.replace('.', ',')
  if ',' in s:
    s = s.rstrip('0')
    s = s.rstrip(',')
  if not currency:
    return s
  elif currency != '' :
    s = s + ' ' + currency
  return s

def visualiseDateTime(dtIn):
  import locale
  locale.setlocale(locale.LC_ALL, settings.LC_ALL)

  if type(dtIn) is date: return dtIn.strftime('%a ') + dtIn.strftime('%d %b %Y').lstrip('0')
  if type(dtIn) is time: return dtIn.strftime('%Hh%M').lstrip('0')
  if type(dtIn) is datetime: return dtIn.strftime('%a ') + dtIn.strftime('%d %b %Y').lstrip('0') + u' - ' + dtIn.strftime('%Hh%M').lstrip('0')


def genIcal(event):
  from icalendar import Calendar, Event, Alarm

  #get details from event instance
  title		= event.title
  desc		= event.title
  start		= datetime.combine(event.when, event.start) 
  end		= datetime.combine(event.when, event.end) 
  location	= event.location
 
  # Timezone to use for our dates - change as needed
  reminderHours = 3

  cal = Calendar()
  cal.add('prodid', '-//CLUSIL calendar application//clusil.lu//')
  cal.add('version', '2.0')
  cal.add('method', "REQUEST")

  vevent = Event()
#  event.add('attendee', self.getEmail())
  vevent.add('organizer', settings.EMAILS['email']['no-reply'])
  vevent.add('status', "confirmed")
  vevent.add('category', "Event")
  vevent.add('summary', title)
  vevent.add('description', desc)
  vevent.add('location', location)
  vevent.add('dtstart', start)
  vevent.add('dtend', end)
  from attendance.functions import gen_hash
  vevent['uid'] = gen_hash(event,settings.EMAILS['email']['no-reply'])[:10] # Generate some unique ID
  vevent.add('priority', 5)
  vevent.add('sequence', 1)
  vevent.add('created', timezone.now())
 
  alarm = Alarm()
  alarm.add("action", "DISPLAY")
  alarm.add('description', "Reminder")
  alarm.add("trigger", timedelta(hours=-reminderHours))
  # The only way to convince Outlook to do it correctly
  alarm.add("TRIGGER;RELATED=START", "-PT{0}H".format(reminderHours))
  vevent.add_component(alarm)
  cal.add_component(vevent)
 
  #gen file to be attached to an email
  from email import MIMEBase, Encoders

  filename = "invite.ics"
  invite = MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
  invite.set_payload( cal.to_ical() )
  Encoders.encode_base64(invite)
  invite.add_header('Content-Description', desc)
  invite.add_header("Content-class", "urn:content-classes:calendarmessage")
  invite.add_header("Filename", filename)
  invite.add_header("Path", filename)

def gen_signup_content():

  return render_to_string(settings.TEMPLATE_CONTENT['reg']['home']['template'], { 
			'title': settings.TEMPLATE_CONTENT['reg']['home']['title'], 
			'desc': settings.TEMPLATE_CONTENT['reg']['home']['desc'], 
			'actions': settings.TEMPLATE_CONTENT['reg']['home']['actions'], 
		})


