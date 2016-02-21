

def get_members_to_validate():
  from .models import Member
  return Member.objects.filter(status=Member.REG)

def get_active_members():
  from .models import Member
  return Member.objects.filter(status=Member.ACT)

def gen_fullname(user):
  return unicode(user.first_name) + u' ' + unicode.upper(user.last_name) + u' (' + unicode(user.email) + u')'

def gen_member_initial(m):
  initial_data = {}

  initial_data['head_of_list'] = gen_fullname(m.head_of_list)
  if m.delegate: initial_data['delagate'] = gen_fullname(m.delagate)
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

