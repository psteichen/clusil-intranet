#coding=utf-8

from datetime import date, datetime
from hashlib import sha256

from django.conf import settings

from members.models import Member
from members.groups.models import Affiliation, Group


##
## supporting functions
##
def gen_mid_hash(salt,message):
  h = sha256()
  h.update(unicode(salt))
  h.update(unicode(message))

  return unicode(h.hexdigest())[:5]

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
  id_part = gen_mid_hash(settings.MEMBER_ID_SALT,msg)
  if add_randomness: 
    msg *= random.uniform(5, 20)
    id_part = gen_mid_hash(settings.MEMBER_ID_SALT,msg)

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

# gen fullname (including organisation if there)
def gen_fullname(m):
  fn = m.head_of_list.first_name + ' ' + unicode.upper(m.head_of_list.last_name)
  if m.type == Member.ORG:
    fn += ' (' + unicode(m.organisation) + ')'
  return fn


def gen_validation_hash(member):
  #hash
  h = sha256()
  h.update(unicode(settings.REG_SALT)) #salt
  h.update(unicode(member.address)) #salt2 (address)
  h.update(unicode(member.head_of_list.email)) #message (email)
  return unicode(h.hexdigest())

def gen_confirmation_link(member):
  from os import path

  c_url = path.join(settings.REG_VAL_URL, gen_validation_hash(member))

  return c_url

