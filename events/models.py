# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField

from members.models import Member

class Event(Model):
  MEET = 0
  OTH = 1
  TYPES = (
    (MEET, 'Meeting'),
    (OTH,  'Other event'),
  )

  title		= CharField(verbose_name='Title',max_length=100)
  when		= DateField(verbose_name='Date')
  time		= TimeField(verbose_name='Starting time')
  location	= CharField(verbose_name='Venue',max_length=500)
  deadline	= DateTimeField(verbose_name='Deadline')
  
  def __unicode__(self):
    return unicode(self.title) + ' du ' + unicode(self.when)


class Invitation(Model):
  event		= ForeignKey(Event)
  message	= CharField(max_length=5000)
  sent		= DateTimeField(blank=True,null=True)
