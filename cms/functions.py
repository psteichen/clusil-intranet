# -*- coding: utf-8 -*-
from datetime import date, datetime, time

from django.conf import settings
from django.template.loader import render_to_string

###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################
def debug(app,message):
  if settings.DEBUG:
    from sys import stderr as errlog
    print >>errlog, 'DEBUG ['+str(app)+']: '+str(message)

def notify_by_email(to,subject,message_content,template='default.txt',attachment=None):
  from django.core.mail import EmailMessage

  if not template: template='default.txt'

  email = EmailMessage(
                subject=subject, 
                from_email=settings.EMAILS['email']['no-reply'], 
                to=[to], 
                cc=[settings.EMAILS['email']['board']] #always Cc to board
          )
  # add default footer (questions, salutation and disclaimer)
  message_content['SALUTATION'] = settings.EMAILS['salutation']
  message_content['DISCLAIMER'] = settings.EMAILS['disclaimer']
  email.body = render_to_string(template,message_content)
  if attachment:
    try: email.attach(attachment)
    except:
      from email.mime.application import MIMEApplication
      if isinstance(attachment, MIMEApplication): email.attach(attachment)
      else: email.attach_file(attachment)
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

