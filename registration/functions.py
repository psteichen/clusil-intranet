from datetime import date

from members.models import Member
from members.groups.models import Affiliation, Group

def gen_member_id():
  num = 0
  #member-id model CLUSIL-YYYY-NNNN
  try:
    ml = str(Member.objects.filter(id__contains=date.today().strftime('%Y')).latest('id'))
    id = ml.split('-')[2].split(' ')[0]
    num = int(id) + 1
  except Member.DoesNotExist:
    num = 1

  mid = 'CLUSIL-%(year)s-%(num)04d' % { 'year': date.today().strftime('%Y'), 'num': num }
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
