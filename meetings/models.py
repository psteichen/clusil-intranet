# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, TimeField, DateTimeField, IntegerField, FileField, EmailField, OneToOneField

from django.contrib.auth.models import Group

from members.models import Member

def rename_report(i,f):
  return 'MEETINGS/'+unicode(i.group.acronym)+'/'+f

class Meeting(Model):
  title		= CharField(max_length=100)
  group		= ForeignKey(Group)
  when		= DateField(verbose_name='Date')
  start		= TimeField(verbose_name='Start time')
  end		= TimeField(verbose_name='End time')
  location	= CharField(max_length=500)
  deadline	= DateTimeField()
  report        = FileField(verbose_name='Minutes', upload_to=rename_report,blank=True,null=True)
  
  def __unicode__(self):
    return unicode(self.title) + ' du ' + unicode(self.when)


def rename_attach(i, f):
  return 'MEETINGS/INVIT/'+unicode(i.meeting.group)+'/'+f

class Invitation(Model):
#  meeting	= ForeignKey(Meeting,primary_key=True)
  meeting	= OneToOneField(Meeting,primary_key=True)
  message	= CharField(max_length=5000,blank=True,null=True)
  attachement   = FileField(upload_to=rename_attach,blank=True,null=True)
  sent		= DateTimeField(blank=True,null=True)

  def __unicode__(self):
    if self.sent:
      return u'Invitations pour: ' + unicode(self.meeting) + u' envoyées à: ' + self.sent.strftime('%Y-%m-%d %H:%M')
    else:
      return u'Invitations pour: ' + unicode(self.meeting) + u' non encore envoyées.'

