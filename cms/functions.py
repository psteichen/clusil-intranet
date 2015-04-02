from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

###############################
# GLOBAL SUPPORTING FUNCTIONS #
###############################

def notify_by_email(sender,to,subject,message_content,template='default.txt',attachment=None):

  if not sender: sender = settings.EMAILS['sender']['default']
  email = EmailMessage(
                subject=subject,
                from_email=sender,
                to=[to],
#                cc=[settings.TEMPLATE_CONTENT['email']['cc'][int(dept)]]
          )
  message_content['FOOTER'] = settings.EMAILS['footer']
  email.body = render_to_string(template,message_content)
  if attachment: email.attach(attachment)
  try:
    email.send()
    return True
  except:
    return False

# rename uploaded files
def rmf(instance, mod, filename=None):
  try:
    orig_name, orig_ext = os.path.splitext(filename)
  except:
    orig_ext = ''

  fn=instance.member_id + os.sep + mod.upper() + '_' + instance.firstname + ' ' + instance.lastname.upper()
  if instance.member_type == 1: # organisation
    fn += ' (' + instance.organisation + ')'

  import unicodedata
  return {'name': unicodedata.normalize('NFKD', fn).encode('ascii','ignore'),'ext': orig_ext}

def show_form(wiz,step,field,const):
  cleaned_data = wiz.get_cleaned_data_for_step(step) or {}
  d = cleaned_data.get(field) or 666
  return int(d) == const

