# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, FileField

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
  agenda	= CharField(verbose_name='Agenda',max_length=500)
  location	= CharField(verbose_name='Venue',max_length=500)
  deadline	= DateTimeField(verbose_name='Registration deadline')
  
  def __unicode__(self):
    return unicode(self.title) + ' [ ' + unicode(self.when) + ' ] '


def rename_attach(i, f):
  return 'EVENTS/INVIT/'+unicode(i.event.title)+'/'+f

class Invitation(Model):
  event		= ForeignKey(Event)
  message	= CharField(max_length=5000)
  attachement   = FileField(upload_to=rename_attach,blank=True,null=True)
  sent		= DateTimeField(blank=True,null=True)

  def __unicode__(self):
    if self.sent:
      return u'Invitations for: ' + unicode(self.event) + u' sent on: ' + self.sent.strftime('%Y-%m-%d %H:%M')
    else:
      return u'Invitations for: ' + unicode(self.event) + u' not sent yet.'

