#coding=utf-8

from datetime import date, datetime
from hashlib import sha256

from django.conf import settings
from django.contrib.auth.models import User

from members.models import Member


##
## supporting functions
##
def gen_hash(salt,message,length,salt2=False):
  h = sha256()
  if salt: h.update(unicode(salt).encode('utf-8')) #salt
  if salt2: h.update(unicode(salt2).encode('utf-8')) #second salt
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

# gen fullname for a user
def gen_user_fullname(u):
  fn = u.first_name + ' ' + unicode.upper(u.last_name) + ' ('+ u.email + ')'
  return fn

def gen_confirmation_link(code):
  from os import path
  c_url = path.join(settings.REG_VAL_URL, code + '/')
  return c_url

def gen_user_list(member):
  out = ''
  out += '''
     Head-of-list: '''+gen_user_fullname(member.head_of_list)
  if member.type == Member.ORG:
    if member.delegate: out += '''
     Delegate: '''+gen_user_fullname(member.delegate)
    for u in member.users.all(): out += '''
     '''+gen_user_fullname(u)
  
  return out

## user creation functions:
def login_exists(username):
  try:
    User.objects.get(username=username)
    return  True
  except User.DoesNotExist:
    return False

def gen_username(fn, ln, pad=0):
  username = ''
  i=0
  j=1
  while i<=pad:
    try:
      username += fn[i]
    except:
      username += unicode(j)
      j += 1
      
    i += 1
  username = unicode.lower(username + ln)
  if login_exists(username): return gen_username(fn, ln, pad+1)
  else: return username

def gen_random_password():
  return User.objects.make_random_password(length=10)

