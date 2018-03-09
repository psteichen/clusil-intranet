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

def notify_by_email(to,subject,message_content,template='default.txt',attachment=None,copy):
  from django.core.mail import EmailMessage
  is_array = lambda var: isinstance(var, (list, tuple))

  if not template: template='default.txt'

  email = EmailMessage(
                subject=subject, 
                from_email=settings.EMAILS['email']['no-reply'], 
                to=[to]
                cc=[copy]
          )
  # add default footer (questions, salutation and disclaimer)
  message_content['SALUTATION'] = settings.EMAILS['salutation']
  message_content['DISCLAIMER'] = settings.EMAILS['disclaimer']
  email.body = render_to_string(template,message_content)
  if attachment:
    if is_array(attachment):
      for a in attachment: attach_to_email(email,a)
    else: attach_to_email(email,attachment)

  try:
    email.send()
    return True
  except:
    return False

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

  return invite
 

############################
# LDAP (for SSO) FUNCTIONS #
############################
def create_ldap_user(user):
  from .models import LdapUser

  lu = None
  try:
    lu = LdapUser.objects.get(username=user.username)
  except LdapUser.DoesNotExist:
    lu = LdapUser(username=user.username)
    lu.first_name = user.first_name
    lu.last_name  = user.last_name
    lu.email      = user.email
    lu.password   = user.password
    lu.save()

  return lu

def add_to_ldap_group(ldap_user,ldap_group_name):
  from .models import LdapGroup

  group = LdapGroup.objects.get(name=ldap_group_name)
  gm = []
  for m in group.members:
    gm.append(m)
  if unicode(ldap_user) != m: gm.append(unicode(ldap_user))

  group.members=gm
  group.save()

def replicate_to_ldap(member):

  #create and add hol and delegate to 'cms' group
  add_to_ldap_group(create_ldap_user(member.head_of_list),'cms')
  if member.delegate: add_to_ldap_group(create_ldap_user(member.delagate),'cms')

  if member.users.count() > 0:
    for u in member.users.all():
      create_ldap_user(u)

