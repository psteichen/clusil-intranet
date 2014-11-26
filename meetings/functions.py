import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from members.functions import get_active_members

################################
# MEEINGS SUPPORTING FUNCTIONS #
################################

def gen_hash(meeting,email,yes=True):
  #hash
  h = hashlib.md5()
  h.update(unicode(email)) #salt (email)
  if yes: h.update('YES') #second salt (YES)
  else: h.update('NO') #second salt (NO)
  h.update(unicode(meeting.num) + unicode(meeting.when)) #message
  return unicode(h.hexdigest())

def gen_attendance_links(meet,e):
#  meeting_url = path.join(settings.MEETINGS_BASE_URL, unicode(meet.num) + '/' )
  meeting_url = path.join(settings.MEETINGS_BASE_URL, unicode(meet.num))
  links = {
    'YES' : path.join(meeting_url, gen_hash(meet,e)),
    'NO'  : path.join(meeting_url, gen_hash(meet,e,False)),
  }

  return links

def gen_invitation_message(template,meeting,member):
  content = {}

  content['title'] = meeting.title
  content['when'] = meeting.when
  content['time'] = meeting.time
  content['location'] = meeting.location
  content['attendance'] = gen_attendance_links(meeting,member.email)

  return render_to_string(template,content)

def gen_meeting_overview(template,meeting):
  content = { 'overview' : settings.TEMPLATE_CONTENT['meetings']['list']['overview'] }

  content['title'] = meeting.title
  content['when'] = meeting.when
  content['time'] = meeting.time
  content['location'] = meeting.location.name
  content['address'] = meeting.location.address
  content['attendance'] = meeting.attendance.all()
  content['excused'] = meeting.excused.all()

  return render_to_string(template,content)

def gen_meeting_initial(m):
  initial_data = {}
  initial_data['title'] = m.title
  initial_data['when'] = m.when
  initial_data['time'] = m.time
  initial_data['location'] = m.location

  return initial_data

def gen_location_initial(l):
  initial_data = {}

  initial_data['name'] = l.name
  initial_data['address'] = l.address

  return initial_data

