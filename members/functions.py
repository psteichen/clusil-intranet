# coding=utf-8

from django.conf import settings
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime



################################
# MEMBERS SUPPORTING FUNCTIONS #
################################

def get_member_from_username(username):
  from django.contrib.auth.models import User
  from members.models import Member

  U = User.objects.get(username=username)
  M = None
  try:
    M = Member.objects.get(head_of_list=U)
  except Member.DoesNotExist:
    pass
  try:
    M = Member.objects.get(delegate=U)
  except Member.DoesNotExist:
    pass
  try:
    M = Member.objects.get(users__in=[U])
  except Member.DoesNotExist:
    pass

  return M

# gen fullname (including organisation if there is)
def gen_member_fullname(m):
  from .models import Member

  fn = m.head_of_list.first_name + ' ' + unicode.upper(m.head_of_list.last_name)
  if m.type == Member.ORG:
    fn += ' (' + unicode(m.organisation) + ')'
  return fn

def get_members_to_validate():
  from .models import Member
  return Member.objects.filter(status=Member.REG)

def get_active_members():
  from .models import Member
  return Member.objects.filter(status=Member.ACT)

def gen_fullname(user):
  try:
    return unicode(user.first_name) + u' ' + unicode.upper(user.last_name)
  except:
    return unicode(user['first_name']) + u' ' + unicode.upper(user['last_name'])

def gen_fulluser(user):
  return unicode(user.first_name) + u' ' + unicode.upper(user.last_name) + u' (' + unicode(user.email) + u')'

def gen_member_initial(m):
  initial_data = {}

  initial_data['head_of_list'] = gen_fullname(m.head_of_list)
  if m.delegate: initial_data['delegate'] = gen_fullname(m.delegate)
  initial_data['address'] = m.address

  return initial_data

def gen_role_initial(r):
  initial_data = {}

  initial_data['title'] = r.title
  initial_data['desc'] = r.desc
  initial_data['member'] = r.member
  initial_data['start_date'] = r.start_date
  initial_data['end_date'] = r.end_date

  return initial_data

def gen_member_id():
  from .models import Member
  num = 0
  #member-id model CLUSIL-YYYY-NNNN
  try:
    ml = str(Member.objects.filter(member_id__contains=date.today().strftime('%Y')).latest('member_id'))
    id = ml.split('-')[2].split(' ')[0]
    num = int(id) + 1
  except Member.DoesNotExist:
    num = 1

  mid = 'CLUSIL-%(year)s-%(num)04d' % { 'year': date.today().strftime('%Y'), 'num': num }
  return mid

def add_group(u,g):
  from groups.models import Group, Affiliation
  group = Affiliation(user=u,group=g)
  group.save()
  default = Affiliation(user=u,group=Group(pk='default'))
  default.save()


def set_cms_perms(user,remove=False):
  from django.contrib.auth.models import Permission

  is_hol_d = Permission.objects.get(codename='MEMBER')
  user.user_permissions.add(is_hol_d)
  user.is_active = True
  if remove: user.user_permissions.remove(is_hol_d)
  user.save()


def gen_user_line(r,u):
  from groups.functions import get_affiliations
  affil = get_affiliations(u)
  ul = { 
	 'role'		: r, 
	 'first_name'	: u.first_name, 
	 'last_name'	: u.last_name, 
	 'email'	: u.email, 
	 'username'	: u.username,
	 'affil'	: affil,
       }
  return ul
  
def get_all_users_for_membership(m):
  users = []
  users.append(gen_user_line('hol',m.head_of_list))
  try:
    users.append(gen_user_line('del',m.delegate))
  except:
    pass
  try:
    for u in m.users.all():
      users.append(gen_user_line('u',u))
  except:
    pass
 
  return users

def get_country_from_address(address):
  from members.models import Address

  c = Address.COUNTRIES[int(address.country)][1]
  if address.country == address.OTH:
    c = unicode(address.c_other)

  return c
 
def gen_member_overview(template,member,actions=False):

  content = { 'overview' : settings.TEMPLATE_CONTENT['members']['details']['overview'] }

  content['title'] = member.id
  content['member'] = member
  content['country'] = get_country_from_address(member.address)
  if actions: content['actions'] = actions
  content['users'] = get_all_users_for_membership(member)

  return render_to_string(template,content)

def gen_renewal_link(code):
  from os import path
  c_url = path.join(settings.RENEW_URL, code + '/')
  return c_url


