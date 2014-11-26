# coding=utf-8

from django.db.models import Model, CharField, DateField, ForeignKey, ManyToManyField, IntegerField, TimeField

from members.models import Member#, Group

class Location(Model):
  name		= CharField(verbose_name='Nom',max_length=100)
  address	= CharField(verbose_name='Adresse',max_length=500)

  def __unicode__(self):
    return unicode(self.name)

class Meeting(Model):
  title		= CharField(max_length=100)
  when		= DateField(verbose_name='Date')
  time		= TimeField()
#  group		= ForeignKey(Group)
  location	= ForeignKey(Location)
  attendance	= ManyToManyField(Member,related_name='attendance',blank=True,null=True)
  excused	= ManyToManyField(Member,related_name='excused',blank=True,null=True)
  
  def __unicode__(self):
    return unicode(self.title) + ' - ' + unicode(self.when)

