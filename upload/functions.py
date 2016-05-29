
from django.conf import settings

from cms.functions import notify_by_email
from registration.functions import gen_hash

def handle_uploaded_file(f,c,subject,to,message,template):
  # create random filename
  fn = unicode('UPL/'+c+'/'+gen_hash(settings.REG_SALT,c,10,to)+'_'+f.name)
  # save file to "campaign" folder
  with open(settings.MEDIA_ROOT+fn, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)

  # send file to "campaign" mailinglist
  message_content = {
    'MESSAGE'	: message,
    'LINK'	: 'https://'+settings.ALLOWED_HOSTS[0]+settings.MEDIA_URL+fn,
  }

#  notify_by_email(None, to, subject, message_content, template, (settings.MEDIA_ROOT+fn, f, f.content_type))
  notify_by_email(None, to, subject, message_content, template, settings.MEDIA_ROOT+fn)
 
