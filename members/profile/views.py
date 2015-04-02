# coding=utf-8
from django.shortcuts import render #uses a RequestContext by default

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string

from cms.functions import notify_by_email

from members.functions import add_group
from members.models import Member
from members.groups.models import Group as WG, Affiliation

from .forms import MemberForm, MemberFormReadOnly, ShortMemberFormReadOnly, WGFormRadio, WGFormCheckBox, UserCreationForm, UserChangeForm, MemberUsersForm, HolForm, DForm

#helper functions
def initial_data(r):
  #get initial data to show
  user_data = {
    'first_name': r.user.first_name,
    'last_name': r.user.last_name,
    'email': r.user.email,
    'username': r.user.username,
  }
  member = Member.objects.get(users=r.user)
  member_data = {
    'member_id': member.member_id,
    'member_type': Member.MEMBER_TYPES[member.member_type][1],
    'lastname': member.lastname,
    'firstname': member.firstname,
    'organisation': member.organisation,
    'email': member.email,
    'address': member.address,
    'postal_code': member.postal_code,
    'town': member.town,
    'country': member.country,
    'head_of_list': member.head_of_list.first_name + ' ' + unicode.upper(member.head_of_list.last_name),
#    'delegate': member.delegate.first_name + ' ' + member.delegate.last_name,
    'users': member.users.all(),
    'student_proof': member.student_proof,
  }
  A = Affiliation.objects.filter(user=r.user)
  wg_data = {
    'wg' : A.values_list('wg',flat=True),
  }
  return { 'member_data': member_data, 'wg_data': wg_data, 'user_data': user_data }

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

def member_is_full(mid):
  m = Member.objects.get(pk=mid)
  users = m.users.count()
  if users >= 6: return True
  else: return False

# index #
#########
@login_required
def index(request):
  request.breadcrumbs( ( ('home','/home/'),
                         ('members','/members/'),
                         ('profile','/members/profile/'),
                        ) )

  return render(request, settings.TEMPLATE_CONTENT['profile']['template'], {
                        'title': settings.TEMPLATE_CONTENT['profile']['title'],
                        'actions': settings.TEMPLATE_CONTENT['profile']['actions'],
                        })

# modify #
###########
@login_required
def modify(r):
  init_data = initial_data(r)
  m_id = init_data['member_data']['member_id']
  m_type = init_data['member_data']['member_type']

  if r.POST: # handle form data & user inputs/mods
    # mode
    mode = r.POST['mode']

    # init data used afterwards even if not changed
    m_fn = init_data['member_data']['firstname']
    m_ln = init_data['member_data']['lastname']
    m_e = init_data['member_data']['email'] 

    u_u = init_data['user_data']['username']
    u_fn = init_data['user_data']['first_name']
    u_ln = init_data['user_data']['last_name']
    u_e = init_data['user_data']['email']
   
    # make instances of post forms to check for changed data
    u = User.objects.get(username=u_u)
    user = UserChangeForm(r.POST,instance=u)
    wgs=r.POST.getlist('wg')

    if user.has_changed() and user.is_valid():
      u_u = user.cleaned_data['username']
      u_fn = user.cleaned_data['first_name']
      u_ln = user.cleaned_data['last_name']
      u_e = user.cleaned_data['email']
      user.save()

    # link user and WG
    toggle_wgs(init_data['wg_data']['wg'],wgs,u)

    # build confirmation email
    message_content = {
      'FULLNAME': u_fn + ' ' + unicode.upper(u_ln),
      'USER': u_u,
      'MEMBER_ID': m_id,
      'USER_MOD': manip_changed_data(user.changed_data,2),
      'WG_MOD': manip_changed_data(wgs,3),
    }
    subject = settings.MAIL_CONFIRMATION['profile']['subject'] % m_id

    if mode == 'ORG_L': # limited data mod: only user and WG data
      # add head-of-list in cc to confirmation email & send
      ok=confirm_by_email(subject,u_e,settings.MAIL_CONFIRMATION['profile']['template'],message_content,None,m_e)
      if not ok:
        return render(r,'profile_org_limited.html', {'member_form': MemberFormReadOnly(initial=init_data['member_data']),'wg_form': WGFormCheckBox(initial=init_data['wg_data']), 'user_form': UserChangeForm(initial=init_data['user_data']), 'error_message': settings.TEMPLATE_CONTENT['error']['email']})
        
    if mode == 'ORG_F' or mode == 'OTHER': # full data mod: member data too
      # make instances of post forms to check for changed data
      m = Member.objects.get(pk=m_id)
      member = MemberForm(r.POST,instance=m)

      if member.has_changed() and member.is_valid():
        m_e = member.cleaned_data['email'] 
        member.save()

        # add changed member data to confirmation email
        message_content['MEMBER_MOD'] = manip_changed_data(member.changed_data,1)

      # send confirmation
      ok=confirm_by_email(subject,u_e,settings.MAIL_CONFIRMATION['profile']['template'],message_content)
      if not ok:
       if mode == 'ORG_F': return render(r,'profile_org_full.html', {'member_form': MemberForm(initial=init_data['member_data']),'wg_form': WGFormCheckBox(initial=init_data['wg_data']), 'user_form': UserChangeForm(initial=init_data['user_data']), 'error_message': settings.TEMPLATE_CONTENT['error']['email']})
       if mode == 'OTHER': return render(r,'profile_other.html', {'member_form': MemberForm(initial=init_data['member_data']),'wg_form': WGFormCheckBox(initial=init_data['wg_data']), 'user_form': UserChangeForm(initial=init_data['user_data']), 'error_message': settings.TEMPLATE_CONTENT['error']['email']})

    #done
    return render(r,'done.html', {'mode': 'updating the CMP for Member: ' + m_id, 'message': render_to_string(settings.MAIL_CONFIRMATION['profile']['template'],message_content)})
  else: # gen form according to member & user type
    # check for profile form mode to use: full or limited (for non-head-of-list users)
    if m_type == Member.MEMBER_TYPES[1][1]: #organisation
      #check if user is head-of-list or delegate
      if is_hol_d(m_id,r.user):
        # head-of-list or delegate -> full(org) profile form
        return render(r,'profile_org_full.html', {'member_form': MemberForm(initial=init_data['member_data']),'wg_form': WGFormCheckBox(initial=init_data['wg_data']), 'user_form': UserChangeForm(initial=init_data['user_data'])})
      else:
        # not head_of_list nor delegate -> limited(org) profile form
        return render(r,'profile_org_limited.html', {'member_form': MemberFormReadOnly(initial=init_data['member_data']),'wg_form': WGFormCheckBox(initial=init_data['wg_data']), 'user_form': UserChangeForm(initial=init_data['user_data'])})
    else:
     # other member type -> full(other) profile form
     return render(r,'profile_other.html', {'member_form': MemberForm(initial=init_data['member_data']),'wg_form': WGFormCheckBox(initial=init_data['wg_data']), 'user_form': UserChangeForm(initial=init_data['user_data'])})


@permission_required('cms.MEMBER')
def adduser(r): # only if membership-type is ORG
  init_data = initial_data(r)
  m_id = init_data['member_data']['member_id']
  m_type = init_data['member_data']['member_type']
  if r.POST:
    user = UserCreationForm(r.POST)
    wg = WGFormRadio(r.POST)
    if user.is_valid() and wg.is_valid():
      m_e = init_data['member_data']['email'] # head-of-list email to send copy
      fn = user.cleaned_data['first_name']
      ln = user.cleaned_data['last_name']
      u = user.cleaned_data['username']
      e = user.cleaned_data['email']
      wg = wg.cleaned_data['wg']

      #save user
      U=user.save()
    
      #add user to member users 
      M=Member.objects.get(pk=m_id)
      M.save()
      M.users.add(U)

      #make the affiliation link
      add_wg(U,wg)

      # build confirmation email
      message_content = {
        'FULLNAME': fn + ' ' + unicode.upper(ln),
        'MEMBER_ID': m_id,
        'LOGIN': u,
        'WG': wg,
      }
      subject = settings.MAIL_CONFIRMATION['adduser']['subject'] % m_id
      # send confirmation email
      ok=confirm_by_email(subject,e,settings.MAIL_CONFIRMATION['adduser']['template'],message_content,None,m_e)
      if not ok:
        return render(r,'profile_org_full.html', {'member_form': ShortMemberFormReadOnly(initial=init_data['member_data']),'wg_form': WGFormRadio(r.POST),'adduser_form': UserCreationForm(r.POST), 'error_message': settings.TEMPLATE_CONTENT['error']['email']})

      return render(r,'done.html', {'mode': 'the creation of another user for Member: ' + m_id, 'message': render_to_string(settings.MAIL_CONFIRMATION['adduser']['template'],message_content)})
    else:
      return render(r,'profile_org_full.html', {'member_form': ShortMemberFormReadOnly(initial=init_data['member_data']),'wg_form': WGFormRadio(r.POST),'adduser_form': UserCreationForm(r.POST), 'error_message': settings.TEMPLATE_CONTENT['error']['gen']})

  else: #no POST data yet, do pre-check or send to form if all fine
    OUT=0
    #prepare "out" message
    message_content = {
      'MEMBER': 'id: ' + m_id + ' - type: ' + m_type,
      'QUESTIONS': settings.MAIL_CONFIRMATION['default']['questions'],
      'SALUTATION': settings.MAIL_CONFIRMATION['default']['salutation'],
    }
    # if not ORG type -> something phishy -> out!
    if not m_type == Member.MEMBER_TYPES[1][1]: #organisation
      OUT=1
      message_content['USERS'] = 'You membership type does only allow one(1) Intrant User.'

    # if already 6 users exist -> out!
    if member_is_full(m_id): 
      OUT=1
      message_content['USERS'] = 'You already hit the maximum of 6 allowed Intranet Users per Membership type "Organisation".'

    if OUT == 1: return render(r,'done.html', {'mode': 'using the CLUSIL Member Intranet', 'message': render_to_string(settings.DONE_MSG['adduser']['template'],message_content)})
    else:
      #show user creation form
      return render(r,'profile_org_full.html', {'member_form': ShortMemberFormReadOnly(initial=init_data['member_data']),'wg_form': WGFormRadio(),'adduser_form': UserCreationForm()})


# remove user
@permission_required('cms.MEMBER')
def tiltuser(r):
  init_data = initial_data(r)
  m_id = init_data['member_data']['member_id']
  m_type = init_data['member_data']['member_type']

  if r.POST:
    users = r.POST.getlist('users')
    for u in users:
      try:
        #desactivate
	U = User.objects.get(pk=u)
 
        message_content = {
          'FULLNAME': U.first_name + ' ' + unicode.upper(U.last_name),
          'LOGIN': U.username,
          'HOL_D': r.user.first_name + ' ' + unicode.upper(r.user.last_name),
        }
        subject=settings.MAIL_CONFIRMATION['tiltuser']['subject'] % U.username
	to=U.email

        #delete user
        U.delete()

        confirm_by_email(subject, to, settings.MAIL_CONFIRMATION['tiltuser']['template'], message_content,None,r.user.email) # copy user that did the action, aka HOL_D

        return render(r,'done.html', {'mode': 'deactivating a User', 'message': render_to_string(settings.MAIL_CONFIRMATION['tiltuser']['template'], message_content)}) 

      except User.DoesNotExist:
        return render(r,'basic.html', {'title': settings.TEMPLATE_CONTENT['profile']['tiltuser']['title'], 'form': MemberUsersForm(initial=init_data['member_data']), 'submit': settings.TEMPLATE_CONTENT['profile']['tiltuser']['submit'], 'error_message': settings.TEMPLATE_CONTENT['error']['tilt']})
  else:
    #no POST data yet -> show user creation form
    return render(r,'basic.html', {'title': settings.TEMPLATE_CONTENT['profile']['tiltuser']['title'], 'form': MemberUsersForm(initial=init_data['member_data']), 'submit': settings.TEMPLATE_CONTENT['profile']['tiltuser']['submit']})


# change head-of-list or delegate
@permission_required('cms.MEMBER')
def chg_hol_d(r):
  init_data = initial_data(r)
  m_id = init_data['member_data']['member_id']
  m_type = init_data['member_data']['member_type']

  if r.POST:
    M = Member.objects.get(pk=m_id)
    message_content= {
      'MEMBER_ID': m_id,
    }

    hol_f = HolForm(r.POST)
    d_f = DForm(r.POST)
    if hol_f.is_valid():
      H = hol_f.cleaned_data['head_of_list']
      M.head_of_list=H

      message_content['H_FULLNAME'] = H.first_name + ' ' + unicode.upper(H.last_name)
      message_content['H_LOGIN'] = H.username
      subject=settings.MAIL_CONFIRMATION['hol']['subject'] % H.first_name + ' ' + unicode.upper(H.last_name)
      confirm_by_email(subject, H.email, settings.MAIL_CONFIRMATION['hol']['template'], message_content)

    d_f = DForm(r.POST)
    if d_f.is_valid():
      D = d_f.cleaned_data['delegate']
      M.delegate=D

      message_content['D_FULLNAME'] = D.first_name + ' ' + unicode.upper(D.last_name)
      message_content['D_LOGIN'] = D.username
      subject=settings.MAIL_CONFIRMATION['deleg']['subject'] % D.first_name + ' ' + unicode.upper(D.last_name)
      confirm_by_email(subject, H.email, settings.MAIL_CONFIRMATION['deleg']['template'], message_content)

    M.save()
    return render(r,'done.html', {'mode': 'changing head-of-list or delegate', 'message': render_to_string(settings.MAIL_CONFIRMATION['hol_d']['template'], message_content)}) 
  else:
    #no POST data yet -> show user creation form
    return render(r,'dual_basic.html', {'title_1': settings.TEMPLATE_CONTENT['profile']['chg_hol_d']['title_1'], 'form_1': HolForm(initial=init_data['member_data']), 'title_2': settings.TEMPLATE_CONTENT['profile']['chg_hol_d']['title_2'], 'form_2': DForm(initial=init_data['member_data']),'submit': settings.TEMPLATE_CONTENT['profile']['chg_hol_d']['submit']})


# invoice viewing
@permission_required('cms.MEMBER')
def invoice(r):
  #no POST data yet -> show user creation form
  return render(r,'basic.html', {'title': settings.TEMPLATE_CONTENT['profile']['tiltuser']['title'], 'form': MemberUsersForm(), 'submit': settings.TEMPLATE_CONTENT['profile']['tiltuser']['submit']})

@login_required
def password(r):
  if r.POST:
    pwd = PasswordChangeForm(r.user,r.POST)
    if pwd.is_valid(): 
      pwd.save()
      message_content = {
        'FULLNAME': r.user.first_name + ' ' + unicode.upper(r.user.last_name),
        'LOGIN': r.user.username,
      }
      subject=settings.MAIL_CONFIRMATION['password']['subject']  % r.user.username
      confirm_by_email(subject, r.user.email, settings.MAIL_CONFIRMATION['password']['template'], message_content)

      return render(r,'done.html', {'mode': 'changing your password', 'message': render_to_string(msettings.MAIL_CONFIRMATION['password']['template'], message_content)})
    else:
      return render(r,'pwd.html', {'pwd_form': PasswordChangeForm(r.user), 'login': r.user.username, 'error_message': settings.TEMPLATE_CONTENT['error']['pwd']})
  else:
    #no POST data yet -> show user creation form
    return render(r,'pwd.html', {'pwd_form': PasswordChangeForm(r.user), 'login': r.user.username })

