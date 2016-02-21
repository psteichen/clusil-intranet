# coding=utf-8

from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from members.functions import add_group, gen_fullname
from members.models import Member, Address
from members.groups.models import Group as WG, Affiliation


############################
# PROFILE helper functions #
############################
def get_member_from_username(username):
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


def get_country_from_address(address):
  c = Address.COUNTRIES[int(address.country)][1]
  if address.country == address.OTH:
    c = unicode(address.c_other)

  return c
 

def member_initial_data(member):
  member_data = {
    'orga'	: member.organisation.name,
    'fn'	: member.head_of_list.first_name,
    'ln'	: member.head_of_list.last_name,
    'email'	: member.head_of_list.email,
    'street'	: member.address.street,
    'pc'	: member.address.postal_code,
    'town'	: member.address.town,
    'country'	: get_country_from_address(member.address),
  }
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


#old stuff
def is_hol_d(mid,u):
  h = Member.objects.filter(pk=mid, head_of_list=u).exists()
  d = Member.objects.filter(pk=mid, delegate=u).exists()
  return h or d

def toggle_wgs(init,current,user):
  i = set(init)
  c = set(current)
  if i!=c: #changes in WG sub
    # delete all and rebuild new subs
    Affiliation.objects.filter(user=user).delete()
    for w in c:
      try: 
        Affiliation.objects.get(user=user,wg=WG(pk=w))
      except Affiliation.DoesNotExist:
        affil = Affiliation(user=user,wg=WG(pk=w))
        affil.save()
    #don't forget to add the default WG: main and board if existed previously
    for w in i:
      if w == 'main' or w == 'board' or w == 'clusix':
        try: 
          Affiliation.objects.get(user=user,wg=WG(pk=w))
        except Affiliation.DoesNotExist:
          affil = Affiliation(user=user,wg=WG(pk=w))
          affil.save()

def manip_changed_data(c,m=0):
  if m == 1: output = '  - in Member data: [ '
  elif m == 2: output = '  - in User data: [ '
  elif m == 3: output = '  - WG subscriptions: [ '
  else: output = '[ '
  if not c: return ''
  for e in c:
    if e != 'password': 
      output += e
      output += ', '
  output += ' ]'
  return output


