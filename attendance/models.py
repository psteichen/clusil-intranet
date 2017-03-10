# coding=utf-8

from django.db.models import Model, ForeignKey, BooleanField, DateTimeField, CharField
from django.contrib.auth.models import User

from meetings.models import Meeting
from events.models import Event

class Meeting_Attendance(Model):
  meeting	= ForeignKey(Meeting)
  user		= ForeignKey(User)
  timestamp	= DateTimeField()
  present	= BooleanField(default=False)
  
  def __unicode__(self):
    present = ''
    if self.present == True:
      present = 'YES'
    elif self.present == False:
      present = 'NO'
    return unicode(self.user) + ' / ' + unicode(self.meeting) + ' (' + unicode(self.timestamp) +') - ' + present

  class Meta:
    unique_together = ( 'user', 'meeting', )

class MtoM(Model):
  meeting	= ForeignKey(Meeting)
  user		= ForeignKey(User)
  yes_hash   	= CharField(max_length=250)
  no_hash   	= CharField(max_length=250)

  class Meta:
    unique_together = ('meeting', 'user')

  def __unicode__(self):
    return unicode(self.meeting) + ' - ' + unicode(self.user)


class Event_Attendance(Model):
  event		= ForeignKey(Event)
  user		= ForeignKey(User)
  timestamp	= DateTimeField()
  present	= BooleanField(default=False)
  
  def __unicode__(self):
    present = ''
    if self.present == True:
      present = 'YES'
    elif self.present == False:
      present = 'NO'
    return unicode(self.user) + ' / ' + unicode(self.event) + ' (' + unicode(self.timestamp) +') - ' + present

  class Meta:
    unique_together = ( 'user', 'event', )

class EtoM(Model):
  event		= ForeignKey(Event)
  user		= ForeignKey(User)
  yes_hash   	= CharField(max_length=250)
  no_hash   	= CharField(max_length=250)

  def __unicode__(self):
    return unicode(self.event) + ' - ' + unicode(self.user)



