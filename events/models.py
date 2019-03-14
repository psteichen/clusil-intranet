# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, FileField, EmailField, ManyToManyField

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
  registration	= CharField(verbose_name='Registration hash',max_length=25)
  
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

class Partner(Model):
  name	= CharField(max_length=150)
  desc	= CharField(max_length=500)
  email	= EmailField()
 
  def __unicode__(self):
    return unicode(self.name)

class Distribution(Model):
  event		= ForeignKey(Event)
  partners	= ManyToManyField(Partner,blank=True)
  others	= CharField(max_length=500,blank=True,null=True)
 
  def __unicode__(self):
    return u'Distribution for: ' + unicode(self.event)


class Participant(Model):
  event		= ForeignKey(Event)
  first_name	= CharField(max_length=150)
  last_name	= CharField(max_length=150)
  email		= EmailField()
  regcode	= CharField(max_length=25)
  affiliation	= ForeignKey(Partner,verbose_name='Partner Affiliation',blank=True,null=True)

  class Meta:
    unique_together = ('event', 'first_name', 'last_name', 'email')

  def __unicode__(self):
    affil = ''
    if self.affiliation: affil = ' ['+unicode(self.affiliation)+']'
    regcode = ' { '+unicode(self.regcode)+' }'
    return unicode(self.first_name) + ' ' + unicode(self.last_name) + ' <' + self.email + '>' + affil + regcode
