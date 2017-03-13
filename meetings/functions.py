# coding=utf-8
import hashlib
from os import path

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime

from attendance.models import Meeting_Attendance
from members.models import Member
from members.functions import get_active_members, gen_fullname

from .models import Invitation

#################################
# MEETINGS SUPPORTING FUNCTIONS #
#################################

def gen_meeting_overview(template,meeting):
  content = { 'overview' : settings.TEMPLATE_CONTENT['meetings']['details']['overview'] }

  content['title'] = meeting.group
  content['topic'] = meeting.title
  content['modify'] = '/meetings/modify/' + unicode(meeting.id)
  content['when'] = visualiseDateTime(meeting.when)
  content['time'] = visualiseDateTime(meeting.start) + ' - ' + visualiseDateTime(meeting.end)
  content['location'] = meeting.location
  if meeting.report:  content['report'] = settings.MEDIA_URL + unicode(meeting.report)
  try:   
    invitation = Invitation.objects.get(meeting=meeting)
    content['message'] = invitation.message
    if invitation.attachement: content['attach'] = settings.MEDIA_URL + unicode(invitation.attachement)
  except: pass
  content['attendance'] = Meeting_Attendance.objects.filter(meeting=meeting,present=True).only('user')
  content['excused'] = Meeting_Attendance.objects.filter(meeting=meeting,present=False).only('user')

  return render_to_string(template,content)

def gen_meeting_initial(m):
  initial_data = {}
  initial_data['title'] = m.title
  initial_data['when'] = m.when
  initial_data['start'] = m.start
  initial_data['end'] = m.end
  initial_data['location'] = m.location
  initial_data['deadline'] = m.deadline

  return initial_data

def gen_invitation_initial(i):
  initial_data = {}
  initial_data['meeting'] = i.meeting
  initial_data['message'] = i.message
  initial_data['attachement'] = i.attachement

  return initial_data

def gen_current_attendance(m):

  initial_data = {}
  initial_data['subscribed'] = Member.objects.filter(meeting_attendance__meeting=m,meeting_attendance__present=True)
  initial_data['excused'] = Member.objects.filter(meeting_attendance__meeting=m,meeting_attendance__present=False)

  return initial_data

def gen_report_message(template,meeting,member):
  content = {}

  content['title'] = meeting.title
  content['when'] = meeting.when
  content['start'] = meeting.start
  content['end'] = meeting.end
  content['location'] = meeting.location

  return render_to_string(template,content)

def gen_meeting_listing(template,meeting):
  content = { 'content' : settings.TEMPLATE_CONTENT['meetings']['listing']['content'] }

  content['title'] = meeting.title
  content['when'] = visualiseDateTime(meeting.when)
  content['time'] = visualiseDateTime(meeting.start) + ' - ' + visualiseDateTime(meeting.end)
  content['location'] = meeting.location.name
  content['address'] = meeting.location.address

  #get attendance / excused
  present = Meeting_Attendance.objects.filter(meeting=meeting,present=True).only('member')
  excused = Meeting_Attendance.objects.filter(meeting=meeting,present=False).only('member')

  content['listing'] = {}
  #header row
  # name (role) / present / excuse / non-excuse / rep / email
  content['listing']['header'] = [
    u'Nom (rôle)', u'présent', u'excusé', u'non excusé', u'Visite hors club', u'E-mail',
  ]

  #records table (alphabetical order on last_name)
  members = Member.objects.all().order_by('last_name')
  content['listing']['members'] = []
  for m in members:
    p = e = n = ''
    for x in present:
      if m.id == x.member.id: p='X'
    for y in excused:
      if m.id == y.member.id: e='X'
    if p == '' and e == '': n='X'
    
    content['listing']['members'].append([
#      	gen_member_fullname_n_role(m), 
      	gen_fullname(m), 
	p, 
	e, 
	n,
	'?', 
	m.email,
    ])

  #resume table
  content['listing']['resume'] = []
  # presents / invités  / total
  P = present.count()
  M = members.all().count()
  E = excused.count()
  N = M-P-E
  content['listing']['resume'].append([
  	u'Présents : &emsp;&emsp;' + unicode(P) + '/' + unicode(M) + '&emsp;&emsp;&emsp;' + unicode(int(round((float(P)/M)*100))) + '%',
  	u'Invités : &emsp;&emsp;' + unicode(I),
  	u'Total : &emsp;&emsp;' + unicode(P+I),
  ])
  # excusés  / non exc. /
  content['listing']['resume'].append([
  	u'Excusés : &emsp;&emsp;' + unicode(E) + '/' + unicode(M) + '&emsp;&emsp;&emsp;' + unicode(int(round((float(E)/M)*100))) + '%',
  	u'Non-excusés : &emsp;&emsp;' + unicode(N) + '/' + unicode(M) + '&emsp;&emsp;&emsp;' + unicode(int(round((float(N)/M)*100))) + '%',
  ])

  return render_to_string(template,content)


