# coding = utf-8

import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from .models import MtoM, EtoM
from events.models import Event

###################################
# ATTENDANCE SUPPORTING FUNCTIONS #
###################################

def gen_hash(event,email,yes=True):
  #hash
  h = hashlib.md5()
  h.update(unicode(email)) #salt (email)
  if yes: h.update('YES') #second salt (YES)
  else: h.update('NO') #second salt (NO)
  h.update(unicode(event.pk) + unicode(event.when)) #message
  return unicode(h.hexdigest())

def gen_attendance_hashes(event,event_type,user):
  yes_hash = gen_hash(event,user.email)
  no_hash = gen_hash(event,user.email,False)
  if event_type == Event.MEET:
    try: MtoM.objects.get(meeting=event,user=user)
    except: 
      mm = MtoM(meeting=event,user=user,yes_hash=yes_hash,no_hash=no_hash)
      mm.save()
  if event_type == Event.OTH:
    try: EtoM.objects.get(event=event,user=user)
    except: 
      em = EtoM(event=event,user=user,yes_hash=yes_hash,no_hash=no_hash)
      em.save()

def get_attendance_hash(e,t,m,yes):
  if t == Event.MEET:
    mm = MtoM.objects.get(meeting=e,user=m)
    if yes: return mm.yes_hash
    else: return mm.no_hash
    
  if t == Event.OTH:
    em = EtoM.objects.get(event=e,user=m)
    if yes: return em.yes_hash
    else: return em.no_hash

def gen_attendance_links(event,event_type,user):
  attendance_url = ''

  if event_type == Event.MEET:
    attendance_url = path.join(settings.MEETINGS_ATTENDANCE_URL, unicode(event.pk))
    
  if event_type == Event.OTH:
    attendance_url = path.join(settings.EVENTS_ATTENDANCE_URL, unicode(event.pk))

  links = {
    'YES' : path.join(attendance_url, get_attendance_hash(event,event_type,user,True)),
    'NO'  : path.join(attendance_url, get_attendance_hash(event,event_type,user,False)),
  }

  return links

def gen_invitation_message(template,event,event_type,user):
  content = {}

  content['title'] = event.title
  if event_type == Event.MEET: content['group'] = event.group
  content['when'] = event.when
  content['time'] = visualiseDateTime(event.start) + ' - ' + visualiseDateTime(event.end)
  content['location'] = event.location
  content['deadline'] = event.deadline
  content['attendance'] = gen_attendance_links(event,event_type,user)

  return render_to_string(template,content)


