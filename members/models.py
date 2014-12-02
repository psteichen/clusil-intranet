from django.db.models import Model, EmailField, DateField, IntegerField, CharField, ForeignKey, ManyToManyField, FileField
from django.db.models.deletion import SET_NULL
from django.contrib.auth.models import User

from members.groups.models import Group

from .functions import gen_user_fullname

# Address model
class Address(Model):
  street 	= CharField(max_length=250)
  num	 	= CharField(max_length=20,blank=True,null=True)
  postal_code 	= CharField(max_length=250)
  town 		= CharField(max_length=250)
  country 	= CharField(max_length=250)
 
  def __unicode__(self):
    return self.street + ' ' + self.num + ' ; ' + self.postal_code + ' ' + self.town + ' ; ' + self.country


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

  ACT = 0
  HON = 1
  STB = 2
  STATUSES = (
    (ACT, 'active'),
    (HON, 'honorary'),
    (STB, 'standby'), #inactive
  )

  id 		= CharField(max_length=25,primary_key=True)
  type 		= IntegerField(choices=MEMBER_TYPES)
  status      	= IntegerField(choices=STATUSES,default=ACT) 
  organisation 	= ForeignKey(Organisation,blank=True,null=True)
  address	= ForeignKey(Address,blank=True,null=True)
  head_of_list 	= ForeignKey(User,related_name='head_of_list+',null=True,on_delete=SET_NULL)
  delegate 	= ForeignKey(User,related_name='delegate+',blank=True,null=True,on_delete=SET_NULL)
  users 	= ManyToManyField(User, related_name='users+')
  student_proof	= FileField(upload_to='board/registration/students/',blank=True,null=True)

  def __unicode__(self):
    o = ''
    if self.type == Member.ORG and self.organisation:
      o += self.organisation + ' - head-of-list: '

    return self.id + ' [ '+ Member.MEMBER_TYPES[self.type][1] + ' ] ' + o + gen_user_fullname(self.head_of_list)


# Role model
class Role(Model):
  title		= CharField(max_length=100)
  user      	= ForeignKey(User) 
  group      	= ForeignKey(Group) 
  start_date    = DateField()
  end_date      = DateField(blank=True,null=True) 

  def __unicode__(self):
    return self.title + ' : ' + gen_user_fullname(self.user)


