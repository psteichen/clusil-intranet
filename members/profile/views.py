# coding=utf-8
from datetime import date

from django.shortcuts import render #uses a RequestContext by default

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password

from django_tables2 import RequestConfig

from cms.functions import notify_by_email, gen_form_errors, group_required

from members.functions import set_hol, unset_hol, is_hol, gen_fullname, get_all_users_for_membership, get_country_from_address, get_member_from_username, set_member, gen_user_initial
from members.models import Member, Renew

from members.groups.functions import affiliate, get_affiliations
from members.groups.models import Group, Affiliation

from accounting.models import Fee
from accounting.functions import generate_invoice

from registration.functions import gen_username, gen_random_password

from .functions import member_initial_data, get_user_choice_list, member_is_full
from .forms import ProfileForm, AffiliateForm, UserForm, UserChangeForm, StudentProofForm
from .tables import InvoiceTable

#################
# PROFILE views #
#################

# profile #
###########
@login_required()
def profile(r):
  r.breadcrumbs( ( 
                  ('member profile','/profile/'),
               ) )

  U = r.user
  M = get_member_from_username(r.user.username)
  if M != None:  
    title = settings.TEMPLATE_CONTENT['profile']['profile']['title'] % { 'member' : M.id, }
    template = settings.TEMPLATE_CONTENT['profile']['profile']['user_overview']['template']
    actions = None
    if is_hol(U): 
      template = settings.TEMPLATE_CONTENT['profile']['profile']['overview']['template']
      actions = settings.TEMPLATE_CONTENT['profile']['profile']['actions']
      if M.type == Member.ORG: actions = settings.TEMPLATE_CONTENT['profile']['profile']['actions_org']

    overview = render_to_string(template, { 
                   			'title'		: title,
					'member'	: M, 
					'country'	: get_country_from_address(M.address), 
					'actions'	: actions, 
					'users'		: get_all_users_for_membership(M), 
					'U'		: U, 
				})

  else: #none-member login, probably an admin
    overview = render_to_string(settings.TEMPLATE_CONTENT['profile']['profile']['admin_overview']['template'], { 
					'user'	: r.user, 
				})

  return render(r, settings.TEMPLATE_CONTENT['profile']['profile']['template'], {
                   'overview'	: overview,
                })


# modify #
###########
@group_required('HEAD-OF-LIST')
def modify(r):
  r.breadcrumbs( (      
                       	('member profile','/profile/'),
                       	('modify','/profile/modify/'),
               ) )
 
  M = get_member_from_username(r.user.username)
  title = settings.TEMPLATE_CONTENT['profile']['modify']['title'].format(id=M.id)

  if r.POST:
 
    pf = ProfileForm(r.POST,r.FILES)
    if pf.is_valid() and pf.has_changed(): 
      for field in pf.changed_data:
        O = None
        if M.type == Member.ORG:
          O = M.organisation

        A = M.address
        H = M.head_of_list
        if M.type == Member.ORG:
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
        if M.type == Member.STD:
          if field == 'sp': #student_proof changed
            M.student_proof = pf.cleaned_data[field]
         
      if M.type == Member.ORG:
        O.save()
      A.save()
      H.save()
      M.save()

      # all fine: done message
      return render(r,settings.TEMPLATE_CONTENT['profile']['modify']['done']['template'], {
			'title'		: settings.TEMPLATE_CONTENT['profile']['modify']['done']['title'].format(id=M.id),
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
    if M.type != Member.ORG:
      del form.fields['orga']
    form.initial = member_initial_data(M)

    return render(r,settings.TEMPLATE_CONTENT['profile']['modify']['template'], {
			'title'		: title,
    			'desc'		: settings.TEMPLATE_CONTENT['profile']['modify']['desc'],
			'form'		: form,
			'submit'	: settings.TEMPLATE_CONTENT['profile']['modify']['submit'],
		 })


# add user #
############
@group_required('HEAD-OF-LIST')
def adduser(r): # only if membership-type is ORG
  r.breadcrumbs( (      
                       	('member profile','/profile/'),
                       	('add user','/profile/adduser/'),
               ) )
 
  M = get_member_from_username(r.user.username)
  template = settings.TEMPLATE_CONTENT['profile']['adduser']['template']
  title = settings.TEMPLATE_CONTENT['profile']['adduser']['title'].format(id=M.id)
  done_template = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['template']

  if r.POST:
    uf = UserForm(r.POST)
    if uf.is_valid():
      #save user
      U=uf.save(commit=False)
      U.username = gen_username(uf.cleaned_data['first_name'],uf.cleaned_data['last_name'])
      U.password = make_password(gen_random_password())
      U.save()
    
      #add user to member users 
      M.save()
      M.users.add(U)

      #add user to ALL group
      set_member(U)
	
      message = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['message'].format(name=gen_fullname(U))
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
      message = settings.TEMPLATE_CONTENT['profile']['adduser']['done']['max'].format(member_id=M.id)

    if message:
      return render(r,done_template, {
				'title'		: title,
				'message'	: message,
			      })

    else:
      #show user creation form
      return render(r,template, {
			'title'		: title,
			'desc'		: settings.TEMPLATE_CONTENT['profile']['adduser']['desc'],
			'submit' 	: settings.TEMPLATE_CONTENT['profile']['adduser']['submit'],
			'form'		: UserForm(),
		   })


# make user the head of list #
##############################
@group_required('HEAD-OF-LIST')
def make_head(r,user):
  r.breadcrumbs( (      
                       	('member profile','/profile/'),
               ) )
 
  M = get_member_from_username(user)
  old_H = M.head_of_list
  new_H = User.objects.get(username=user)

  #set new head-of-list
  M.head_of_list = new_H
  if M.delegate and M.delegate == new_H: 
    M.delegate = None
  M.save()
  M.users.add(old_H) #add old head to users
  M.users.remove(new_H) #remove new head from users

  #set perms
  set_hol(new_H) #set as head
  unset_hol(old_H) #remove as head


  title = settings.TEMPLATE_CONTENT['profile']['make_head']['title'].format(id=M.id)
  template = settings.TEMPLATE_CONTENT['profile']['make_head']['template']
  message = settings.TEMPLATE_CONTENT['profile']['make_head']['message'].format(head=gen_fullname(M.head_of_list))

  return render(r,template, {
			'title'		: title,
			'message'	: message,
	       })



# make user the delegate #
##########################
@group_required('HEAD-OF-LIST')
def make_delegate(r,user):
  r.breadcrumbs( (      
                       	('member profile','/profile/'),
               ) )
 
  M = get_member_from_username(user)
  old_D = M.delegate
  new_D = User.objects.get(username=user)

  #set new delegate
  M.delegate = new_D
  if M.head_of_list == new_D: 
    M.head_of_list = None
  M.save()
  if old_D: M.users.add(old_D) #add old delegate to users
  M.users.remove(new_D) #remove new delegate from users

  #set perms
  if old_D: unset_hol(old_D) #remove perms for old delegate
  set_hol(new_D) #set perms for new delegate


  title = settings.TEMPLATE_CONTENT['profile']['make_delegate']['title'].format(id=M.id)
  template = settings.TEMPLATE_CONTENT['profile']['make_delegate']['template']
  message = settings.TEMPLATE_CONTENT['profile']['make_delegate']['message'].format(head=gen_fullname(M.delegate))

  return render(r,template, {
			'title'		: title,
			'message'	: message,
	       })


# modify user #
###############
@login_required()
def moduser(r,user):
  r.breadcrumbs( (      
                       	('member profile','/profile/'),
               ) )
 
  U = User.objects.get(username=user)
  title 	= settings.TEMPLATE_CONTENT['profile']['moduser']['title'].format(name=gen_fullname(U))
  template 	= settings.TEMPLATE_CONTENT['profile']['moduser']['template']
  done_title 	= settings.TEMPLATE_CONTENT['profile']['moduser']['done']['title'].format(name=gen_fullname(U))
  done_template = settings.TEMPLATE_CONTENT['profile']['moduser']['done']['template']

  if r.POST:
    uf = UserForm(r.POST,instance=U)
    if uf.is_valid() and uf.has_changed():
      U = uf.save()

      #all fine
      return render(r,done_template, {
			'title'		: done_title,
		   })

    else: #from not valid -> error
      return render(r,done_template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ' + gen_form_errors(uf),
		   })

  else:
    #no POST data yet -> show working groups form
    form = UserForm()
    form.initial = gen_user_initial(U)
    form.instance = U

    return render(r,template, {
			'title'	: title,
  			'desc'	: settings.TEMPLATE_CONTENT['profile']['moduser']['desc'].format(name=gen_fullname(U)),
  			'submit': settings.TEMPLATE_CONTENT['profile']['moduser']['submit'],
			'form'	: form,
		   })



# remove user #
###############
@group_required('HEAD-OF-LIST')
def rmuser(r,user,really=False): # only if membership-type is ORG
  r.breadcrumbs( (      
                       	('member profile','/profile/'),
               ) )
 
  title 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['title']
  template 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['template']
  message 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['message']

  done_title 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['done']['title']
  done_template 	= settings.TEMPLATE_CONTENT['profile']['rmuser']['done']['template']
  done_message 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['done']['message']

  error_title 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['error']['title']
  error_message 	= settings.TEMPLATE_CONTENT['profile']['rmuser']['error']['message']

  M = get_member_from_username(user)
  U = User.objects.get(username=user)
  #check if hol
  if not r.user.username == M.head_of_list.username:
    return render(r,done_template, {
			'title'		: error_title,
                	'error_message'	: error_message,
		 })
  
  #check if REALLY want to delete user
  if really == 'REALLY':
    msg = done_message.format(
				name	= gen_fullname(U),
				email	= U.email,
				login	= U.username
			     )
    U.delete()
    return render(r,done_template, {
			'title'		: done_title,
			'message'	: msg,
	       })

  else: #show user to delete and give a second chance to decide
    return render(r,template, {
			'title'		: title,
			'message'	: message.format(
								name	= gen_fullname(U),
								email	= U.email,
								login	= U.username,
								affil	= get_affiliations(U),
								url	= '/profile/rmuser/'+U.username+'/REALLY/'
							),
		 })


# invoice #
###########
@group_required('HEAD-OF-LIST')
def invoice(r):
  r.breadcrumbs( ( 
                       	('member profile','/profile/'),
                       	('invoices','/profile/invoice/'),
               ) )

  template = settings.TEMPLATE_CONTENT['profile']['invoice']['template']
  done_template = settings.TEMPLATE_CONTENT['profile']['invoice']['done']['template']
  M = get_member_from_username(r.user.username)
  if M != None:  
    title = settings.TEMPLATE_CONTENT['profile']['invoice']['title'] % { 'member' : M.id, }
    desc = settings.TEMPLATE_CONTENT['profile']['invoice']['desc']
    actions = settings.TEMPLATE_CONTENT['profile']['invoice']['actions']
 
    table = InvoiceTable(Fee.objects.filter(member=M).order_by('-year'))
    RequestConfig(r, paginate={"per_page": 75}).configure(table)

    return render(r, template, {
			'title'		: title,
			'desc'		: desc,
			'actions'	: actions,
       	            	'table'		: table,
                  })

  else: #none-member login -> probably an admin
    return render(r, done_template, {
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'],
		   })


# new invoice #
###############
@group_required('HEAD-OF-LIST')
def new_invoice(r):
  r.breadcrumbs( ( 
                       	('member profile','/profile/'),
                       	('invoices','/profile/invoice/'),
               ) )
  M = get_member_from_username(r.user.username)
  generate_invoice(M)

  template = settings.TEMPLATE_CONTENT['profile']['newinv']['template']
  title = settings.TEMPLATE_CONTENT['profile']['newinv']['title'].format(id=M.id)
  message = settings.TEMPLATE_CONTENT['profile']['newinv']['message'].format(head=gen_fullname(M.head_of_list),year=date.today().strftime('%Y'))
  return render(r, template, {
			'title'		: title,
			'message'	: message,
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
      notify_by_email(r.user.email, subject, message_content, settings.MAIL_CONFIRMATION['password']['template'])

      return render(r,'done.html', {'mode': 'changing your password', 'message': render_to_string(msettings.MAIL_CONFIRMATION['password']['template'], message_content)})
    else:
      return render(r,'pwd.html', {'pwd_form': PasswordChangeForm(r.user), 'login': r.user.username, 'error_message': settings.TEMPLATE_CONTENT['error']['pwd']})
  else:
    #no POST data yet -> show user creation form
    return render(r,'pwd.html', {'pwd_form': PasswordChangeForm(r.user), 'login': r.user.username })


# renew validation #
####################
def validate_renewal(renew,member,year):
  # save renewal as OK
  renew.ok = True 
  renew.save()

  # save Member as active
  member.status = Member.ACT
  member.save()

  # generate invoice for given year (this will generate and send the invoice)
  generate_invoice(member,year)



def renew(r, code):

  title 		= settings.TEMPLATE_CONTENT['profile']['renew']['title']
  template		= settings.TEMPLATE_CONTENT['profile']['renew']['template']
  done_message		= settings.TEMPLATE_CONTENT['profile']['renew']['done_message']
  error_message		= settings.TEMPLATE_CONTENT['profile']['renew']['error_message']

  if r.POST: #get student_proof
    spf = StudentProofForm(r.POST,r.FILES)
    if spf.is_valid():
      code = spf.cleaned_data['code']
      R = Renew.objects.get(renew_code=code)
      M = R.member
      y = R.year

      if spf.cleaned_data['student_proof']:
        M.student_proof = spf.cleaned_data['student_proof']
      else: #switch to "individual" type and remove student proof
        M.type = Member.IND
        M.student_proof = None
        M.save()

      #all fine
      validate_renewal(R,M,y)
  
      message = done_message.format(name=gen_fullname(M.head_of_list),member_id=M.pk)
      return render(r, template, {
				'title'		: title,
	                   	'message'	: message,
                   })

    else: #from not valid -> error
      return render(r,template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ' + gen_form_errors(uf),
		   })

  try:
    # if hash code match: it's a renewal to be validated
    R = Renew.objects.get(renew_code=code)
    if R.ok:
      return render(r, template, {
                   'title'		: title,
                   'error_message'	: error_message,
               })

    M = R.member
    y = R.year

    # check if student
    if M.type == Member.STD:
      # ask for student_proof renewal 
      form = StudentProofForm(initial={'code': code, 'member': M.pk, })

      return render(r,settings.TEMPLATE_CONTENT['profile']['renew']['sp']['template'], {
  			'title'	: settings.TEMPLATE_CONTENT['profile']['renew']['sp']['title'].format(year=y),
  			'desc'	: settings.TEMPLATE_CONTENT['profile']['renew']['sp']['desc'].format(year=y),
  			'submit': settings.TEMPLATE_CONTENT['profile']['renew']['sp']['submit'],
			'form'	: form,
		   })
    else:
      validate_renewal(R,M,y)
      message = done_message.format(name=gen_fullname(M.head_of_list),member_id=M.pk)
      return render(r, template, {
				'title'		: title,
	                   	'message'	: message,
                   })

  except Renew.DoesNotExist:
    # else: error
    return render(r, template, {
                   'title'		: title,
                   'error_message'	: error_message,
               })
 

