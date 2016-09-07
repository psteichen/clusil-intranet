
import datetime
import locale
from sys import stderr as errlog
from os.path import splitext
from re import search, findall
import csv

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from cms.functions import notify_by_email

from registration.functions import gen_hash, gen_username, gen_random_password

from members.models import Member, Address
from meetings.models import Meeting


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
 

def import_data(ty,data):

#TODO

  error = False
#  for line in csv.DictReader(data,delimiter='\t',quoting=csv.QUOTE_NONE):
  for l in csv.DictReader(data.read().splitlines(),delimiter=';',quoting=csv.QUOTE_NONE):
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))
#  for line in c_data:
#    l = findall(r'\"(.+?)\"',str(line))

    Model = None
    try:
      if ty == "members":
#       Model = Member.objects.get(first_name=l[1],last_name=l[0],email=l[6])
        Model = Member.objects.get(first_name=unicode(l['VIRNUMM']),last_name=unicode(l['NUMM']),email=unicode(l['EMAIL']))
      if ty == "calendar": Model = Meeting.objects.get(title=unicode(l[0]),when=unicode(l[1]),time=unicode(l[2]))
    except:
      if ty == "members":
        A = Address (
                address         = unicode(l['ADRESS']),
                postal_code     = unicode(l['CP']),
                location        = unicode(l['DUERF']),
                country         = unicode(l['LAND'])
        )
        Model = Member (
                        first_name      = unicode(l['VIRNUMM']),
                        last_name       = unicode(l['NUMM']),
                        address         = A,
                        email           = unicode(l['EMAIL'])
                )
        # create user
        user = User.objects.create_user(gen_username(Model.first_name,Model.last_name), Model.email, make_password(gen_random_password()))
        Model.user = user
      if ty == "calendar":
        Model = Meeting (
                        title           = unicode(l[0]),
                        when            = unicode(l[1]),
                        time            = unicode(l[2])
                )

        # check/create location
        location = None
        try:
          location = Location.objects.get(name=l[3])
        except Location.DoesNotExist:
          location = Location (name=l[3])

        Model.location = location

      Model.save()

  return error

