# coding=utf-8
from django.shortcuts import render #uses a RequestContext by default

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string

from django_tables2 import RequestConfig

from cms.functions import notify_by_email, gen_form_errors

from members.functions import add_group, set_cms_perms, gen_fullname, get_all_users_for_membership, get_country_from_address
from members.models import Member

from members.groups.functions import affiliate, get_affiliations
from members.groups.models import Group, Affiliation

from accounting.models import Fee

from .functions import get_member_from_username, member_initial_data, get_user_choice_list, member_is_full
from .forms import ProfileForm, AffiliateForm, UserCreationForm, UserChangeForm
from .tables import InvoiceTable

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
					'users'		: get_all_users_for_membership(M), 
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
  r.breadcrumbs( (      
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('affiliate user','/profile/affiluser/'+user),
               ) )
 
  M = get_member_from_username(user)
  U = User.objects.get(username=user)
  title = settings.TEMPLATE_CONTENT['profile']['affiluser']['title'].format(name=gen_fullname(U))
  template = settings.TEMPLATE_CONTENT['profile']['affiluser']['template']
  done_title = settings.TEMPLATE_CONTENT['profile']['affiluser']['done']['title'].format(name=gen_fullname(U))
  done_template = settings.TEMPLATE_CONTENT['profile']['affiluser']['done']['template']

  if r.POST:
    af = AffiliateForm(r.POST)
    if af.is_valid() and af.has_changed():
      # get selected wgs and affiliate to user
      WGs = af.cleaned_data['wgs']
      AGs = af.cleaned_data['ags']
      TLs = af.cleaned_data['tls']
#TODO: add ldap sync
      for wg in WGs: 
        affiliate(U,wg)
      for ag in AGs: 
        affiliate(U,ag)
      for tl in TLs: 
        affiliate(U,tl)


      #all fine -> show working groups form
      message = settings.TEMPLATE_CONTENT['profile']['affiluser']['done']['message'].format(name=gen_fullname(U),groups=get_affiliations(U))
      return render(r,done_template, {
			'title'		: done_title,
			'message'	: message,
		   })

    else: #from not valid -> error
      return render(r,done_template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ' + gen_form_errors(af),
		   })


  else:
    #no POST data yet -> show working groups form
    form = AffiliateForm()
    Affils = Affiliation.objects.filter(user=U)
    init = { 'wgs': [], 'ags': [], 'tls': [], }
    for a in Affils:
      if a.group.type == Group.WG: init['wgs'].append(a.group.pk)
      if a.group.type == Group.AG: init['ags'].append(a.group.pk)
      if a.group.type == Group.TL: init['tls'].append(a.group.pk)
    form.initial = init

    return render(r,template, {
			'title'	: title,
  			'desc'	: settings.TEMPLATE_CONTENT['profile']['affiluser']['desc'].format(name=gen_fullname(U)),
  			'submit': settings.TEMPLATE_CONTENT['profile']['affiluser']['submit'],
			'form'	: form,
		   })


# make user the head of list #
##############################
@permission_required('cms.MEMBER')
def make_head(r,user):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('make head-of-list','/profile/make_head/'+user),
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
                       	('make delegate','/profile/make_delegate/'+user),
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


#TODO
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


# invoice #
###########
@permission_required('cms.MEMBER')
def invoice(r):
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('member profile','/profile/'),
                       	('invoice','/profile/invoice/'),
               ) )

  template = settings.TEMPLATE_CONTENT['profile']['invoice']['template']
  done_template = settings.TEMPLATE_CONTENT['profile']['invoice']['done']['template']
  M = get_member_from_username(r.user.username)
  if M != None:  
    title = settings.TEMPLATE_CONTENT['profile']['invoice']['title'] % { 'member' : M.id, }
    desc = settings.TEMPLATE_CONTENT['profile']['invoice']['desc']
 
    table = InvoiceTable(Fee.objects.filter(member=M).order_by('-year'))
    RequestConfig(r, paginate={"per_page": 75}).configure(table)

    return render(r, template, {
			'title'		: title,
			'desc'		: desc,
       	            	'table'		: table,
                  })

  else: #none-member login -> error
    return render(r, done_template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'],
		   })


# password #
############
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

