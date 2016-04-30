import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from attendance.models import Event_Attendance
from members.functions import get_active_members

from .models import Invitation

###############################
# EVENTS SUPPORTING FUNCTIONS #
###############################

def gen_event_overview(template,event):
  content = { 'overview' : settings.TEMPLATE_CONTENT['events']['details']['overview'] }

  content['title'] = event.title
  content['when'] = visualiseDateTime(event.when)
  content['time'] = visualiseDateTime(event.time)
  content['location'] = event.location
  I = Invitation.objects.get(event=event)
  content['invitation'] = I.message
  if I.attachement: content['attachement'] = I.attachement

  return render_to_string(template,content)

def gen_event_initial(e):
  initial_data = {}
  initial_data['title'] = e.title
  initial_data['when'] = e.when
  initial_data['time'] = e.time
  initial_data['location'] = e.location
  initial_data['deadline'] = e.deadline

  return initial_data

def gen_current_attendance(e):

  initial_data = {}
  initial_data['subscribe'] = Event_Attendance.objects.filter(event=e,present=True).only('user')
  initial_data['excuse'] = Event_Attendance.objects.filter(event=e,present=False).only('user')

  return initial_data

