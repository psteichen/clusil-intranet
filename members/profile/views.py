# coding=utf-8
from django.shortcuts import render #uses a RequestContext by default

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string

from cms.functions import notify_by_email

from members.functions import add_group, set_cms_perms, gen_fullname
from members.models import Member
from members.groups.models import Group as WG, Affiliation

from .functions import get_member_from_username, get_country_from_address, member_initial_data, get_user_choice_list, member_is_full
from .forms import ProfileForm, MemberFormReadOnly, ShortMemberFormReadOnly, WGFormRadio, WGFormCheckBox, UserCreationForm, UserChangeForm, MemberUsersForm, HolForm, DForm

################
# MEMBER views #
################

# profile #
###########
@permission_required('cms.MEMBER')
def profile(r):
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('member profile','/profile/'),
               ) )

  M = get_member_from_username(r.user.username)
  if M != None:  
    title = settings.TEMPLATE_CONTENT['profile']['profile']['title'] % { 'member' : M.id, }
    actions = settings.TEMPLATE_CONTENT['profile']['profile']['actions']
    if M.type == Member.ORG: actions = settings.TEMPLATE_CONTENT['profile']['profile']['actions_org']
    overview = render_to_string(settings.TEMPLATE_CONTENT['profile']['profile']['overview']['template'], { 
                   			'title'		: title,
					'member'	: M, 
					'country'	: get_country_from_address(M.address), 
					'actions'	: actions, 
				})
  else: #none-member login, probably an admin
    overview = render_to_string(settings.TEMPLATE_CONTENT['profile']['profile']['user_overview']['template'], { 
					'user'	: r.user, 
				})

  return render(r, settings.TEMPLATE_CONTENT['profile']['profile']['template'], {
                   'overview'	: overview,
                })


# modify #
###########
@permission_required('cms.MEMBER')
def modify(r):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('modify','/profile/modify/'),
               ) )
 
  M = get_member_from_username(r.user.username)
  title = settings.TEMPLATE_CONTENT['profile']['modify']['title'].format(id=M.id)

  if r.POST:
 
    pf = ProfileForm(r.POST,r.FILES)
    if pf.is_valid() and pf.has_changed(): 
      for field in pf.changed_data:
        O = M.organisation
        A = M.address
        if field == 'orga': #organisation name changed
          O.name = pf.cleaned_data[field]
        if field == 'fn': #first_name of head_of_list changed
          H.first_name = pf.cleaned_data[field]
        if field == 'ln': #last_name of head_of_list changed
          H.last_name = pf.cleaned_data[field]
        if field == 'email': #email of head_of_list changed
          H.email = pf.cleaned_data[field]
        if field == 'street': #street changed
          A.street = pf.cleaned_data[field]
        if field == 'pc': #postal_code changed
          A.postal_code = pf.cleaned_data[field]
        if field == 'town': #town changed
          A.town = pf.cleaned_data[field]
        if field == 'country': #country changed
          A.c_other = pf.cleaned_data[field]
        if field == 'sp': #student_proof changed
          M.student_proof = pf.cleaned_data[field]
         
        O.save()
        A.save()
        M.save()

        # all fine: done message
        return render(r,settings.TEMPLATE_CONTENT['profile']['modify']['done']['template'], {
			'title'		: title,
                	'message'	: settings.TEMPLATE_CONTENT['profile']['modify']['done']['message'] + ' ;<br/> '.join([f for f in pf.changed_data]),
		     })

        
    else: #form not valid -> error
      return render(r,settings.TEMPLATE_CONTENT['profile']['modify']['done']['template'], {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in pf.errors]),
		   })
 
  else: # gen form according to member & user type

    form = ProfileForm()
    if M.type != Member.STD:
      del form.fields['sp']
    form.initial = member_initial_data(M)

    return render(r,settings.TEMPLATE_CONTENT['profile']['modify']['template'], {
			'title'		: title,
    			'desc'		: settings.TEMPLATE_CONTENT['profile']['modify']['desc'],
			'form'		: form,
			'submit'	: settings.TEMPLATE_CONTENT['profile']['modify']['submit'],
		 })


# add user #
############
@permission_required('cms.MEMBER')
def adduser(r): # only if membership-type is ORG
  r.breadcrumbs( (      
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('add user','/profile/adduser/'),
               ) )
 
  M = get_member_from_username(r.user.username)
  title = settings.TEMPLATE_CONTENT['profile']['adduser']['title'].format(id=M.id)
  done_template = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['template']

  if r.POST:
    uf = UserCreationForm(r.POST)
    if uf.is_valid():
      #save user
      U=uf.save(commit=False)
      U.username = gen_username(user.first_name,user.last_name)
      U.password = make_password(gen_random_password())
      U.save()
    
      #add user to member users 
      M.save()
      M.users.add(U)
	
      message = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['message'].format(user=gen_fullname(U))
      return render(r,done_template, {
			'title'		: title,
			'message'	: message,
		   })

    else: #from not valid -> error
      return render(r,done_template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in uf.errors]),
		   })

  else: #no POST data yet, do pre-check or send to form if all fine
    message=False
    # if not ORG type -> something phishy -> out!
    if M.type != Member.ORG:
      message = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['no_org']

    # if max users exist -> out!
    if member_is_full(M): 
      message = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['max']

    if message:
      return render(r,done_template, {
				'title'		: title,
				'message'	: message,
			      })

    else:
      #show user creation form
      return render(r,done_template, {
			'title'	: title,
  			'desc'	: settings.TEMPLATE_CONTENT['profile']['adduser']['desc'],
			'form'	: UserCreationForm(),
		   })


# affiliate user #
##################
@permission_required('cms.MEMBER')
def affiluser(r,user):
#TODO!

  if r.POST:
  else:
    #no POST data yet -> show working groups form
    return render(r,done_template, {
			'title'	: title,
  			'desc'	: settings.TEMPLATE_CONTENT['profile']['affiluser']['desc'],
			'form'	: WGFormCheckBox(),
		   })


# make user the head of list #
##############################
@permission_required('cms.MEMBER')
def make_head(r,user):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('make head-of-list','/profile/make_head/'),
               ) )
 
  M = get_member_from_username(user)
  old_H = M.head_of_list
  new_H = User.objects.get(username=user)

  #set new head-of-list
  M.head_of_list = new_H
  M.save()
  M.users.add(old_H) #add old head to users
  M.users.remove(new_H) #remove new head from users

  #set perms
  set_cms_perms(new_H) #set perms for new head
  set_cms_perms(old_H,True) #remove perms for old head


  title = settings.TEMPLATE_CONTENT['profile']['make_head']['title'].format(id=M.id)
  template = settings.TEMPLATE_CONTENT['profile']['make_head']['template']
  message = settings.TEMPLATE_CONTENT['profile']['make_head']['message'].format(head=gen_fullname(M.head_of_list))

  return render(r,template, {
			'title'		: title,
			'message'	: message,
	       })



# make user the delegate #
##########################
@permission_required('cms.MEMBER')
def make_delegate(r,user):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('make delegate','/profile/make_delegate/'),
               ) )
 
  M = get_member_from_username(user)
  old_D = M.delegate
  new_D = User.objects.get(username=user)

  #set new delegate
  M.delegate = new_D
  M.save()
  if old_D: M.users.add(old_D) #add old delegate to users
  M.users.remove(new_D) #remove new delegate from users

  #set perms
  if old_D: set_cms_perms(old_D,True) #remove perms for old delegate
  set_cms_perms(new_D) #set perms for new delegate


  title = settings.TEMPLATE_CONTENT['profile']['make_delegate']['title'].format(id=M.id)
  template = settings.TEMPLATE_CONTENT['profile']['make_delegate']['template']
  message = settings.TEMPLATE_CONTENT['profile']['make_delegate']['message'].format(head=gen_fullname(M.delegate))

  return render(r,template, {
			'title'		: title,
			'message'	: message,
	       })


# remove user #
###############
@permission_required('cms.MEMBER')
def rmuser(r,user): # only if membership-type is ORG
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
        subject=settings.MAIL_CONFIRMATION['rmuser']['subject'] % U.username
	to=U.email

        #delete user
        U.delete()

        confirm_by_email(subject, to, settings.MAIL_CONFIRMATION['rmuser']['template'], message_content,None,r.user.email) # copy user that did the action, aka HOL_D

        return render(r,'done.html', {'mode': 'deactivating a User', 'message': render_to_string(settings.MAIL_CONFIRMATION['rmuser']['template'], message_content)}) 

      except User.DoesNotExist:
        return render(r,'basic.html', {'title': settings.TEMPLATE_CONTENT['profile']['rmuser']['title'], 'form': MemberUsersForm(initial=init_data['member_data']), 'submit': settings.TEMPLATE_CONTENT['profile']['rmuser']['submit'], 'error_message': settings.TEMPLATE_CONTENT['error']['rm']})
  else:
    #no POST data yet -> show user creation form
    return render(r,'basic.html', {'title': settings.TEMPLATE_CONTENT['profile']['rmuser']['title'], 'form': MemberUsersForm(initial=init_data['member_data']), 'submit': settings.TEMPLATE_CONTENT['profile']['rmuser']['submit']})


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
  return render(r,'basic.html', {'title': settings.TEMPLATE_CONTENT['profile']['rmuser']['title'], 'form': MemberUsersForm(), 'submit': settings.TEMPLATE_CONTENT['profile']['rmuser']['submit']})

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

