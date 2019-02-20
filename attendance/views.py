#
# coding=utf-8
#
from datetime import date, datetime

from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User

from cms.functions import notify_by_email, visualiseDateTime

from members.models import Member
from members.functions import get_active_members, gen_fullname, get_all_users_for_membership, get_member_from_username
from members.functions import get_group_members

from meetings.models import Meeting
from events.models import Event

from .functions import gen_hash
from .models import Meeting_Attendance, MtoM, Event_Attendance, EtoM


####################
# ATTENDANCE VIEWS #
####################

# attendance (FAST) #
#####################
def attendance_fast(r, event_type, event_id, attendance_hash):
  E = M = title = deadline = e_yes = e_no = message = member = actions = None
  notify = False
  e_message = None
  A = None

  if event_type == 'meetings':
    M = Meeting.objects.get(pk=event_id)
    deadline = M.deadline
    title = settings.TEMPLATE_CONTENT['attendance']['meeting']['title'] % { 'meeting': M.group, }
    e_yes = settings.TEMPLATE_CONTENT['attendance']['meeting']['email']['yes'] % { 'meeting': M.title, }
    e_no = settings.TEMPLATE_CONTENT['attendance']['meeting']['email']['no'] % { 'meeting': M.title, }
    
    if timezone.now() >= deadline:
      message = settings.TEMPLATE_CONTENT['attendance']['too_late']
    else:
      mTm = None
      try:
        mTm = MtoM.objects.get(yes_hash=attendance_hash)
        # it's a YES
        M = mTm.meeting
        U = mTm.user
        try:
          A = Meeting_Attendance.objects.get(meeting=M,user=U)
        except:
          A = Meeting_Attendance(meeting=M,user=U)

        A.present = True
        A.timestamp = timezone.now()
        A.save()
        notify=True
        member=get_member_from_username(U.username)
        message = settings.TEMPLATE_CONTENT['attendance']['yes'] % { 'name': gen_fullname(U), }
        #add meeting information to the confirmation message
        message += settings.TEMPLATE_CONTENT['attendance']['details'] % { 'title': M.title, 'when': M.when, 'time': visualiseDateTime(M.start) + ' - ' + visualiseDateTime(M.end), 'location': M.location, }
        actions = settings.TEMPLATE_CONTENT['attendance']['actions']
        e_message = e_yes
      except:
        try:
          mTm = MtoM.objects.get(no_hash=attendance_hash) 
          # it's a NO
          M = mTm.meeting
          U = mTm.user
          try:
            A = Meeting_Attendance.objects.get(meeting=M,user=U)
          except:
            A = Meeting_Attendance(meeting=M,user=U)

          A.present = False
          A.timestamp = timezone.now()
          A.save()
          notify=True
          message = settings.TEMPLATE_CONTENT['attendance']['no'] % { 'name': gen_fullname(U), }
          e_message = e_no
        except:
          pass

  if event_type == 'events':
    E = Event.objects.get(pk=event_id)
    G = E.group
    deadline = E.deadline
    title = settings.TEMPLATE_CONTENT['attendance']['event']['title'] % { 'event': E.title, }
    e_yes = settings.TEMPLATE_CONTENT['attendance']['event']['email']['yes'] % { 'event': E.title, }
    e_no = settings.TEMPLATE_CONTENT['attendance']['event']['email']['no'] % { 'event': E.title, }

    if timezone.now() >= deadline:
      message = settings.TEMPLATE_CONTENT['attendance']['too_late']
    else:
      eTm = None
      try:
        eTm = EtoM.objects.get(yes_hash=attendance_hash)
        # it's a YES
        E = eTm.event
        U = eTm.user
        try:
          A = Event_Attendance.objects.get(event=E,user=U)
        except:
          A = Event_Attendance(event=E,user=U)

        A.present = True
        A.timestamp = timezone.now()
        A.save()
        notify=True
        member=get_member_from_username(U.username)
        message = settings.TEMPLATE_CONTENT['attendance']['yes'] % { 'name': gen_fullname(U), }
        actions = settings.TEMPLATE_CONTENT['attendance']['actions']
        e_message = e_yes
      except:
        try:
          eTm = EtoM.objects.get(no_hash=attendance_hash) 
          # it's a NO
          E = eTm.event
          U = eTm.user
          try:
            A = Event_Attendance.objects.get(event=E,user=U)
          except:
            A = Event_Attendance(event=E,user=U)

          A.present = False
          A.timestamp = timezone.now()
          A.save()
          notify=True
          message = settings.TEMPLATE_CONTENT['attendance']['no'] % { 'name': gen_fullname(U), }
          e_message = e_no
        except:
          pass


    if notify:
      #notify by email
      message_content = {
            'FULLNAME'	: gen_fullname(U),
            'MESSAGE'	: e_message,
      }
      #send email
      ok=notify_by_email(U.email,title,message_content)

    #set meeting: id and member_id for invitee link
    if actions:
      actions[0]['url'] += str(M.pk)+'/'+str(member.id)

  return render(r, settings.TEMPLATE_CONTENT['attendance']['template'], {
                   'title': title,
                   'actions' : actions,
                   'message': message,
               })

    
 
# attendance #
##############
def attendance(r, event_type, event_id, attendance_hash):
  E = M = title = deadline = e_yes = e_no = message = member = actions = None

  if event_type == 'meetings':
    M = Meeting.objects.get(pk=event_id)
    deadline = M.deadline
    title = settings.TEMPLATE_CONTENT['attendance']['meeting']['title'] % { 'meeting': M.group, }
    e_yes = settings.TEMPLATE_CONTENT['attendance']['meeting']['email']['yes'] % { 'meeting': M.title, }
    e_no = settings.TEMPLATE_CONTENT['attendance']['meeting']['email']['no'] % { 'meeting': M.title, }
  if event_type == 'events':
    E = Event.objects.get(pk=event_id)
    G = E.group
    deadline = E.deadline
    title = settings.TEMPLATE_CONTENT['attendance']['event']['title'] % { 'event': E.title, }
    e_yes = settings.TEMPLATE_CONTENT['attendance']['event']['email']['yes'] % { 'event': E.title, }
    e_no = settings.TEMPLATE_CONTENT['attendance']['event']['email']['no'] % { 'event': E.title, }

  if timezone.now() >= deadline:
    message = settings.TEMPLATE_CONTENT['attendance']['too_late']
  else:
    for m in get_active_members():
      notify = False
      e_message = None
      A = None

      if event_type == 'meetings':
        for U in get_group_members(M.group):

          try:
            A = Meeting_Attendance.objects.get(meeting=M,user=U)
          except:
            A = Meeting_Attendance(meeting=M,user=U)

          mTm = MtoM.objects.get(meeting=M,user=U)
          if attendance_hash == mTm.yes_hash:
            # it's a YES
            A.present = True
            A.timestamp = timezone.now()
            A.save()
            notify=True
            member=m
            message = settings.TEMPLATE_CONTENT['attendance']['yes'] % { 'name': gen_fullname(U), }
            #add meeting information to the confirmation message
            message += settings.TEMPLATE_CONTENT['attendance']['details'] % { 'title': M.title, 'when': M.when, 'time': visualiseDateTime(M.start) + ' - ' + visualiseDateTime(M.end), 'location': M.location, }
            actions = settings.TEMPLATE_CONTENT['attendance']['actions']
            e_message = e_yes
  
          if attendance_hash == mTm.no_hash:
            # it's a NO
            A.present = False
            A.timestamp = timezone.now()
            A.save()
            notify=True
            message = settings.TEMPLATE_CONTENT['attendance']['no'] % { 'name': gen_fullname(U), }
            e_message = e_no


      elif event_type == 'events':
        for u in get_all_users_for_membership(m):
	  U = User.objects.get(username=u['username'])

          try:
            A = Event_Attendance.objects.get(event=E,user=U)
          except:
            A = Event_Attendance(event=E,user=U)

          eTm = EtoM.objects.get(event=E,user=U)
          if attendance_hash == eTm.yes_hash:
            # it's a YES
            A.present = True
            A.timestamp = timezone.now()
            A.save()
            notify=True
            member=m
            message = settings.TEMPLATE_CONTENT['attendance']['yes'] % { 'name': gen_fullname(U), }
            actions = settings.TEMPLATE_CONTENT['attendance']['actions']
            e_message = e_yes
    
          if attendance_hash == eTm.no_hash:
            # it's a NO
            A.present = False
            A.timestamp = timezone.now()
            A.save()
            notify=True
            message = settings.TEMPLATE_CONTENT['attendance']['no'] % { 'name': gen_fullname(U), }
            e_message = e_no
  
  
        if notify:
          #notify by email
          message_content = {
            'FULLNAME'	: gen_fullname(U),
            'MESSAGE'	: e_message,
          }
          #send email
          ok=notify_by_email(U.email,title,message_content)


  #set meeting: id and member_id for invitee link
  if actions:
    actions[0]['url'] += str(M.pk)+'/'+str(member.id)

  return render(r, settings.TEMPLATE_CONTENT['attendance']['template'], {
                   'title': title,
                   'actions' : actions,
                   'message': message,
               })

