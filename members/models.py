from django.db.models import Model, EmailField, DateField, IntegerField, CharField, ForeignKey, ManyToManyField, FileField, BooleanField
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User, Group
from django.conf import settings

from .functions import gen_fulluser

# Address model
class Address(Model):
  LU	= 0
  FR	= 1
  BE	= 2
  DE	= 3
  NL	= 4
  OTH	= 5
  COUNTRIES = (
    (LU	,'Luxembourg'),
    (FR	,'France'),
    (BE	,'Belgium'),
    (DE	,'Germany'),
    (NL	,'The Netherlands'),
    (OTH,'Other'),
  )
  street 	= CharField(verbose_name="Num & street",max_length=250)
  postal_code 	= CharField(max_length=250)
  town 		= CharField(max_length=250)
  country 	= IntegerField(choices=COUNTRIES,default=LU)
  c_other 	= CharField(max_length=250,blank=True,null=True)

  def gen_country(self):
    c = self.COUNTRIES[int(self.country)][1]
    if self.country == self.OTH:
      c = unicode(self.c_other)

    return c

  def __unicode__(self):
    return self.street + ' ' + self.postal_code + ' ' + self.town +  ' ' + self.gen_country()


# Organisation model
class Organisation(Model):
  name 		= CharField(max_length=250)
  address	= ForeignKey(Address)


def rename_sp(i,f):
  return 'REG/students/'+i.id+'_'+f

# Member model
class Member(Model):
  IND = 0
  ORG = 1
  STD = 2
  MEMBER_TYPES = (
    (IND, 'individual'),
    (ORG, 'organisation'),
    (STD, 'student'),
  )

  SINGLE 	= 1
  ORG_6 	= 6
  ORG_12 	= 12
  ORG_18 	= 18
  ORG_OPEN 	= 99
  MEMBER_LEVELS = (
    (SINGLE, 	'single'),
    (ORG_6, 	'6 users'),
    (ORG_12, 	'12 users'),
    (ORG_18, 	'18 users'),
    (ORG_OPEN, 	'more users'),# needs to be set manually
  )

  REG = 0
  ACT = 1
  INA = 2
  HON = 3
  STATUSES = (
    (REG, 'registered'),
    (ACT, 'active'),
    (INA, 'inactive'),
    (HON, 'honorary'),
  )


  id 		= CharField(max_length=25,primary_key=True)
  type 		= IntegerField(choices=MEMBER_TYPES)
  lvl 		= IntegerField(choices=MEMBER_LEVELS,default=SINGLE)
  status      	= IntegerField(choices=STATUSES,default=REG) 
  organisation 	= ForeignKey(Organisation,blank=True,null=True)
  address	= ForeignKey(Address,blank=True,null=True)
  head_of_list 	= ForeignKey(User,related_name='head_of_list+',null=True,on_delete=SET_NULL)
  delegate 	= ForeignKey(User,related_name='delegate+',blank=True,null=True,on_delete=SET_NULL)
  users 	= ManyToManyField(User, related_name='users+',blank=True)
  student_proof	= FileField(upload_to=rename_sp,blank=True,null=True)

  def gen_name(self):
    o = ''
    hol = ''
    t = self.MEMBER_TYPES[int(self.type)][1]

    if self.head_of_list: hol = gen_fulluser(self.head_of_list)
    if self.type == Member.ORG and self.organisation:
      o += unicode(self.organisation.name) + ' - head-of-list: ' + hol
    else:
      o += hol

    return self.id + ' [ ' + t + ' ] - ' + o

  def nb_users(self):
    nb = 0
    if self.head_of_list:
      nb+=1
    if self.delegate:
      nb+=1
    nb += self.users.count()
    return nb


settings.FEE = {
    Member.IND	: 100,
    Member.STD 	: 25,
    Member.ORG_6: 400,
    Member.ORG_12: 700,
    Member.ORG_18 : 1000,
}

# Renew model
class Renew(Model):
  member	= ForeignKey(Member) 
  year      	= CharField(max_length=4)
  renew_code   	= CharField(max_length=15)
  ok	   	= BooleanField(default=False)

  class Meta:
    unique_together = ('member', 'year',)

  def __unicode__(self):
    status=''
    if self.ok: status=' - OK'
    return unicode(self.member.pk) + ' [' + self.year + ']' + ' (' + self.renew_code + ')' + status


# Role model
class Role(Model):
  title		= CharField(max_length=100)
  user      	= ForeignKey(User) 
  group    	= ForeignKey(Group,blank=True,null=True) 
  start_date    = DateField(blank=True,null=True)
  end_date      = DateField(blank=True,null=True) 

  def __unicode__(self):
    return self.title + ' : ' + gen_fulluser(self.user)


