import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from attendance.models import Event_Attendance
from members.functions import get_active_members

from .models import Invitation, Participant

###############################
# EVENTS SUPPORTING FUNCTIONS #
###############################

def get_event_attendance(event):
  out=''
  for p in Participant.objects.filter(event=event):
    out += '''
''' + unicode(p)
  
  return out

def gen_event_overview(overview,event,p=False):
  content = { 'overview' : overview }

  content['title'] = event.title
  content['when'] = visualiseDateTime(event.when)
  content['time'] = visualiseDateTime(event.time)
  content['location'] = event.location
  content['agenda'] = event.agenda
  I = Invitation.objects.get(event=event)
  content['invitation'] = I.message
  if I.attachement: content['attachement'] = I.attachement
  content['attendance'] = get_event_attendance(event)
  content['registration'] = settings.EVENTS_REG_BASE_URL + event.registration
  if p: content['regcode'] = p.regcode

  return render_to_string(overview['template'],content)

def gen_event_initial(e):
  initial_data = {}
  initial_data['title'] = e.title
  initial_data['when'] = e.when
  initial_data['time'] = e.time
  initial_data['location'] = e.location
  initial_data['deadline'] = e.deadline

  return initial_data

def gen_reg_hash(event):
  #hash
  h = hashlib.md5()
  h.update(unicode(event.agenda)) #salt
  h.update(unicode(event.title) + unicode(event.when)) #message
  return unicode(h.hexdigest()[:10])

def gen_reg_code(e,p):
  #hash
  h = hashlib.md5()
  h.update(unicode(p.email)) #salt
  h.update(unicode(e.title) + unicode(e.when)) #message
  return unicode(h.hexdigest()[:15])

def gen_registration_message(template,event,participant):
  content = {}

  content['title'] = event.title
  content['when'] = event.when
  content['time'] = visualiseDateTime(event.time)
  content['location'] = event.location
  content['agenda'] = event.agenda
  content['code'] = participant.regcode

  return render_to_string(template,content)


