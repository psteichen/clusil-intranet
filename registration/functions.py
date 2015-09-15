#coding=utf-8

from datetime import date, datetime
from hashlib import sha256

from django.conf import settings

from members.models import Member
from members.groups.models import Affiliation, Group


##
## supporting functions
##
def gen_hash(salt,message,length,salt2=False):
  h = sha256()
  if salt: h.update(unicode(salt)) #salt
  if salt2: h.update(unicode(salt2)) #second salt
  h.update(unicode(message)) #message

  return unicode(h.hexdigest())[:int(length)]

def member_id_exists(mid):
  try:
    Member.objects.get(pk=mid)
    return True
  except Member.DoesNotExist:
    return False


##
## functions used in views
##
def gen_member_id(add_randomness=False):
  msg = datetime.today()
  if add_randomness: 
    msg *= random.uniform(5, 20)

  id_part = gen_hash(settings.MEMBER_ID_SALT,msg,5)

  if member_id_exists(id_part):
    id_part = gen_member_id(True)

  mid = 'CLUSIL-%(year)s-%(id)05s' % { 'year': date.today().strftime('%Y'), 'id': id_part }
  return mid

def add_to_groups(user,groups):
  for g in groups:
    Affiliation(user=user,group=g)

  #add to default group
  d = Affiliation(user=user,group=Group(pk='main'))
  d.save()

# gen fullname (including organisation if there is)
def gen_member_fullname(m):
  fn = m.head_of_list.first_name + ' ' + unicode.upper(m.head_of_list.last_name)
  if m.type == Member.ORG:
    fn += ' (' + unicode(m.organisation) + ')'
  return fn

def gen_confirmation_link(code):
  from os import path
  c_url = path.join(settings.REG_VAL_URL, code + '/')
  return c_url

