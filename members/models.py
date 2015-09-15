from django.db.models import Model, EmailField, DateField, IntegerField, CharField, ForeignKey, ManyToManyField, FileField
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User

from members.groups.models import Group

from .functions import gen_fullname

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
 
  def __unicode__(self):
    c = self.COUNTRIES[int(self.country)][1]
    if self.country == self.OTH:
      c = unicode(self.c_other)

    return self.street + ' ; ' + self.postal_code + ' ' + self.town + ' ; ' + c


# Organisation model
class Organisation(Model):
  name 		= CharField(max_length=250)
  address	= ForeignKey(Address)

  def __unicode__(self):
    return self.name + ' (' + unicode(self.address) + ')'


# Member model
class Member(Model):
  IND = 0
  ORG = 1
  STD = 2
  MEMBER_TYPES = (
    (IND, 'Individual'),
    (ORG, 'Organisation'),
    (STD, 'Student'),
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
  status      	= IntegerField(choices=STATUSES,default=REG) 
  organisation 	= ForeignKey(Organisation,blank=True,null=True)
  address	= ForeignKey(Address,blank=True,null=True)
  head_of_list 	= ForeignKey(User,related_name='head_of_list+',null=True,on_delete=SET_NULL)
  delegate 	= ForeignKey(User,related_name='delegate+',blank=True,null=True,on_delete=SET_NULL)
  users 	= ManyToManyField(User, related_name='users+')
  student_proof	= FileField(upload_to='board/registration/students/',blank=True,null=True)

  def __unicode__(self):
    o = ''
    if self.type == Member.ORG and self.organisation:
      o += unicode(self.organisation) + ' - head-of-list: ' + gen_fullname(self.head_of_list)

    return self.id + ' [ '+ Member.MEMBER_TYPES[self.type][1] + ' ] ' + o


# Role model
class Role(Model):
  title		= CharField(max_length=100)
  user      	= ForeignKey(User) 
  group      	= ForeignKey(Group) 
  start_date    = DateField()
  end_date      = DateField(blank=True,null=True) 

  def __unicode__(self):
    return self.title + ' : ' + gen_fullname(self.user)


