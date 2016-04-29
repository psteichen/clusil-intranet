# -*- coding: utf-8 -*-
from datetime import date, datetime, time

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################

def notify_by_email(sender,to,subject,message_content,template='default.txt',attachment=None):

  board = settings.EMAILS['sender']['board'] #board

  if not sender: sender = settings.EMAILS['sender']['no-reply'] #default
  else: sender = settings.EMAILS['sender'][unicode(sender)]
  email = EmailMessage(
                subject		= '[CLUSIL] ' + subject,
                from_email	= sender,
                to		= [to],
                cc		= [board]
          )
  message_content['SALUTATION'] = settings.EMAILS['salutation']
  message_content['DISCLAIMER'] = settings.EMAILS['disclaimer']

  if not template: email.body = render_to_string('default.txt',message_content)
  else: email.body = render_to_string(template,message_content)
  if attachment: email.attach(attachment)
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

  if type(dtIn) is date: return dtIn.strftime('%a le ') + dtIn.strftime('%d %b %Y').lstrip('0')
  if type(dtIn) is time: return dtIn.strftime('%Hh%M').lstrip('0')
  if type(dtIn) is datetime: return dtIn.strftime('%a le ') + dtIn.strftime('%d %b %Y').lstrip('0') + u' à ' + dtIn.strftime('%Hh%M').lstrip('0')


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

