# coding=utf-8

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string

from cms.functions import visualiseDateTime


################################
# MEMBERS SUPPORTING FUNCTIONS #
################################

def get_member_from_username(username):
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

def gen_user_initial(u):
  initial_data = {}

  initial_data['first_name'] = u.first_name
  initial_data['last_name'] =  u.last_name
  initial_data['email'] = u.email

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

# Group setting functions
def set_group(u,g):
  u.groups.add(g)
  u.save()

def unset_group(u,g):
  u.groups.remove(g)
  u.save()

def set_member(u):
  members = Group.objects.get(name='Members')
  set_group(u,members)

def is_member(user):
  return user.groups.filter(name='Members').exists()

def set_hol(u):
  members = Group.objects.get(name='HeadOfLists')
  set_group(u,members)

def unset_hol(u):
  members = Group.objects.get(name='HeadOfLists')
  unset_group(u,members)

def is_hol(user):
  if user.is_superuser: return True
  else:
    return user.groups.filter(name='HeadOfLists').exists()


def set_board(u):
  members = Group.objects.get(name='Board')
  set_group(u,members)
 
def is_board(user):
  if user.is_superuser: return True
  else:
    return user.groups.filter(name='Board').exists()


def set_admin(u):
  members = Group.objects.get(name='Admins')
  set_group(u,members)
 
def is_admin(user):
  if user.is_superuser: return True
  else:
    return user.groups.filter(name='Admins').exists()



def gen_user_line(r,u):
  ul = { 
	 'role'		: r, 
	 'first_name'	: u.first_name, 
	 'last_name'	: u.last_name, 
	 'email'	: u.email, 
	 'username'	: u.username,
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
  content['media_url'] = settings.MEDIA_URL

  return render_to_string(template,content)

def gen_renewal_link(code):
  from os import path
  c_url = path.join(settings.RENEW_URL, code + '/')
  return c_url


def activate_member(member):
  from django.contrib.auth.models import Permission, User
  from members.models import Member
  from groups.models import Group
  from groups.functions import affiliate
  from accounting.functions import generate_invoice
  from attendance.functions import gen_attendance_hashes
  from events.models import Event
  from meetings.models import Meeting

  # set head-of-list (and delegate)
  set_hol(member.head_of_list)
  if member.delegate: set_hol(member.delegate)

  # member confirmation Ok -> replicate Users to LDAP
  #replicate_to_ldap(member)

  # save Member as active
  member.status = Member.ACT
  member.save()

  # set all users as Member
  for u in get_all_users_for_membership(member):
    U = User.objects.get(username=u['username'])
    set_member(U)

    # gen attendance hashes for existing events
    for e in Event.objects.all():
      gen_attendance_hashes(e,Event.OTH,U)
    # and meetings
    for m in Meeting.objects.all():
      gen_attendance_hashes(m,Event.MEET,U)

  # generate invoice (this will generate and send the invoice)
  generate_invoice(member)


def member_initial_data(member):
  member_data = {
    'fn'	: member.head_of_list.first_name,
    'ln'	: member.head_of_list.last_name,
    'email'	: member.head_of_list.email,
    'street'	: member.address.street,
    'pc'	: member.address.postal_code,
    'town'	: member.address.town,
    'country'	: get_country_from_address(member.address),
  }
  if member.type == Member.ORG: member_data['orga'] = member.organisation.name
  if member.type == Member.STD: member_data['sp'] = member.student_proof

  return member_data


def get_user_choice_list(member):
  from members.functions import gen_fullname

  user_list = [('','None identified')]
  hol = member.head_of_list
  user_list.append((hol,gen_fullname(hol)),)
  if member.delegate: 
    d = member.delegate
    user_list.append((d,gen_fullname(hol)),)
  if member.users.all(): 
    users = member.users
    for u in users.all():
      user_list.append((u,gen_fullname(u)),)

  return tuple(user_list)


def member_is_full(member):
  users = member.users.count() + 1
  if member.delegate: users += 1
  if users >= member.lvl: return True
  else: return False


