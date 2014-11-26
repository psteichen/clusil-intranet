import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings


###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################
def debug(app,message):
  if settings.DEBUG:
    from sys import stderr as errlog
    print >>errlog, 'DEBUG ['+str(app)+']: '+str(message)

def notify_by_email(dept,subject,to,message_content,template='default.txt',attachment=None):
  from django.core.mail import EmailMessage

  email = EmailMessage(
                subject=subject, 
                from_email=settings.TEMPLATE_CONTENT['email']['no-reply'], 
                to=[to], 
                cc=[settings.TEMPLATE_CONTENT['email']['cc'][int(dept)]]
          )
  # add default footer (questions, salutation and disclaimer)
  message_content['QUESTIONS'] = settings.TEMPLATE_CONTENT['email']['questions']
  message_content['FOOTER'] = settings.TEMPLATE_CONTENT['email']['footer']
  email.body = render_to_string(template,message_content)
  if attachment: email.attach(attachment)
  try:
    email.send()
    return True
  except:
    return False

def gen_fullname_for_user(user):
  return user.first_name + ' ' + unicode.upper(user.last_name)

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
  if type(dtIn) is datetime.date: return dtIn.strftime('%d. %b %Y').lstrip('0')
  if type(dtIn) is datetime.time: return dtIn.strftime('%H:%M').lstrip('0')
  if type(dtIn) is datetime.datetime: return dtIn.strftime('%d. %b %Y %H:%M').lstrip('0')


################
# GLOBAL VIEWS #
################
def open_home(r):
  return render(r, settings.TEMPLATE_CONTENT['open_home']['template'], { 
			'title': settings.TEMPLATE_CONTENT['open_home']['title'], 
			'actions': settings.TEMPLATE_CONTENT['open_home']['actions'], 
		})

def documentation(r):
  r.breadcrumbs( ( ('home','/'),
                   ('documentation','/documentation/'),
               ) )

  return render(r, settings.TEMPLATE_CONTENT['documentation']['template'], { 
			'title': settings.TEMPLATE_CONTENT['documentation']['title'], 
			'desc': settings.TEMPLATE_CONTENT['documentation']['desc'], 
			'docs': settings.TEMPLATE_CONTENT['documentation']['docs'], 
		})

@login_required
def home(r):
  return render(r, settings.TEMPLATE_CONTENT['home']['template'], { 
			'title': settings.TEMPLATE_CONTENT['home']['title'], 
			'actions': settings.TEMPLATE_CONTENT['home']['actions'], 
		})

