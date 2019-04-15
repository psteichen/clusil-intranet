# coding=utf-8
from datetime import date
from random import random

from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required

from formtools.wizard.views import SessionWizardView
from django_tables2  import RequestConfig

from cms.functions import show_form, notify_by_email, gen_form_errors, debug, group_required

from registration.functions import gen_hash, gen_username, gen_random_password

from accounting.models import Fee
from accounting.functions import generate_invoice

from attendance.functions import gen_attendance_hashes
from members.functions import set_member, set_hol, unset_hol, gen_fullname, get_all_users_for_membership, get_country_from_address, get_member_from_username, gen_user_initial
from members.models import Member, Renew

from meetings.models import Meeting
from events.models import Event

from .profile.tables import InvoiceTable

from .functions import gen_member_initial, gen_role_initial, gen_fullname, gen_member_overview, get_active_members, gen_renewal_link, gen_member_fullname, member_initial_data, get_user_choice_list, member_is_full
from .forms import UserForm, UserChangeForm, MemberForm, RoleForm
from .models import Member, Role, Renew
from .tables  import MemberTable, InvoiceTable


################
# MEMBER views #
################

# list #
#########
@group_required('BOARD')
def list(request):
  request.breadcrumbs( ( ('board','/board/'),
                         ('members','/members/'),
                        ) )

  table = MemberTable(Member.objects.all().order_by('status'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['members']['template'], {
                        'title': settings.TEMPLATE_CONTENT['members']['title'],
                        'actions': settings.TEMPLATE_CONTENT['members']['actions'],
                        'table': table,
                        })


# renew #
#########
@group_required('BOARD')
def renew(r):
  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('annual renewal','/members/renew/'),
               ) )

  year = date.today().strftime('%Y')

  template 		= settings.TEMPLATE_CONTENT['members']['renew']['template']
  title 		= settings.TEMPLATE_CONTENT['members']['renew']['title'].format(year=year)
  email_template 	= settings.TEMPLATE_CONTENT['members']['renew']['email']['template']
  email_title 		= settings.TEMPLATE_CONTENT['members']['renew']['email']['title'].format(year=year)

  m_list = '<ul>'

  #loop throu all active members and send membership renewal request
  for m in get_active_members():
    try:
      f = Fee.objects.get(member=m,year=year)
    except:
      # if member didn't get an invoice yet for this year
#TODO:
# renewal link only for students to renew student_proof
# for all others send invoice directly, cf members.profile.renew()
#
      salt2=float(year)
      renew_hash_code = gen_hash(settings.RENEW_SALT,unicode(m.head_of_list.email)+unicode(m.address).encode('ascii', 'ignore'),15,salt2)
      # build request mail
      message_content = {
        'FULLNAME'	: gen_member_fullname(m),
        'YEAR'		: year,
	'LINK'		: gen_renewal_link(renew_hash_code),
      }

      debug('members.renew','renewing member: '+unicode(m))

      # send confirmation
      ok=notify_by_email(m.head_of_list.email,email_title,message_content,email_template,copy=True)
      if not ok:
        return render(r, template, { 
				'mode': 'Error in email request', 
				'message': settings.TEMPLATE_CONTENT['error']['email'],
		   })

      try:
        renew = Renew.objects.get(member=m,year=year)
        renew.ok = False
        renew.save()
      except Renew.DoesNotExist:
        renew = Renew(member=m,year=year,renew_code=renew_hash_code)
        renew.save()

      m_list += '<li>'+gen_member_fullname(m)+'</li>'
   
  m_list += '</ul>'
  # all fine
  return render(r, template, { 
			'title'		: title,
        		'message'	: m_list,
	       })
 



# details #
###########
@group_required('BOARD')
def details(r, member_id):
  member = Member.objects.get(id=member_id)

  mid = unicode(member.id)

  r.breadcrumbs( ( 
			('board','/board/'),
                   	('members','/members/'),
                   	('details of member: '+unicode(mid),'/members/details/'+mid+'/'),
               ) )

  actions = settings.TEMPLATE_CONTENT['members']['details']['overview']['actions']
  for a in actions:
    a['url'] = a['url'].format(mid)
  message = gen_member_overview(settings.TEMPLATE_CONTENT['members']['details']['overview']['template'],member,actions)

  return render(r, settings.TEMPLATE_CONTENT['members']['details']['template'], {
                   'message': message,
                })


# modify #
##########

#modify helper functions
def show_role_form(wizard):
  return show_form(wizard,'member','role',True)

#modify formwizard
class ModifyMemberWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyMemberWizard, self).get_context_data(form=form, **kwargs)

    step = self.steps.current

    M = None
    if self.kwargs['member_id']:
      M = Member.objects.get(pk=self.kwargs['member_id'])
      #add breadcrumbs to context
      self.request.breadcrumbs( ( 
					('board','/board/'),
        	 	                ('member','/members/'),
	        	       	        ('modify a member','/members/modify/'),
                            ) )
    else:
      M = Member.objects.get(head_of_list=self.request.user)
      #add breadcrumbs to context
      self.request.breadcrumbs( ( 
					('home','/home/'),
	        	       	        ('member profile','/members/profile/'),
	        	       	        ('modify member profile','/members/profile/modify/'),
                            ) )

    if step != None:
      context.update({'title': settings.TEMPLATE_CONTENT['members']['modify']['title']})
      if step != 'list': context.update({'step_title': settings.TEMPLATE_CONTENT['members']['modify'][self.steps.current]['title'] + ' - ' + M.id})
      else : context.update({'step_title': settings.TEMPLATE_CONTENT['members']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['members']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyMemberWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    M = None
    if self.kwargs['member_id']:
      M = Member.objects.get(pk=self.kwargs['member_id'])
    else:
      M = Member.objects.get(head_of_list=self.request.user)

    if step == 'member':
      form.initial = gen_member_initial(M)
      form.instance = M

    if step == 'role':
      role = Role.objects.get(member=M.id)
      form.initial = gen_role_initial(role)
      form.instance = role

    return form

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( ('home','/home/'),
         	                ('member','/members/'),
                	        ('modify a member','/members/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['members']['modify']['done']['template']

    M = R = None
    mf = form_dict['member_id']
    role = mf.cleaned_data['role']
    if role: rf = form_dict['role']

    if mf.is_valid():
      M = mf.save()

    if role: 
      if rf.is_valid():
        R = rf.save()

    title = settings.TEMPLATE_CONTENT['members']['modify']['done']['title'] % M

    return render(self.request, template, {
				'title': title,
                 })


# invoice #
###########
@group_required('MEMBER')
def invoice(r, member_id):
  M = Member.objects.get(id=member_id)
  mid = unicode(M.id)

  r.breadcrumbs( ( 
			('home','/home/'),
                       	('members','/members/'),
                       	('invoices - '+mid,'/members/invoice/'+mid+'/'),
               ) )

  template = settings.TEMPLATE_CONTENT['profile']['invoice']['template']
  done_template = settings.TEMPLATE_CONTENT['profile']['invoice']['done']['template']
  if M != None:  
    title = settings.TEMPLATE_CONTENT['profile']['invoice']['title'] % { 'member' : mid, }
    desc = settings.TEMPLATE_CONTENT['profile']['invoice']['desc']
    admin_actions = settings.TEMPLATE_CONTENT['profile']['invoice']['admin_actions']
    for aa in admin_actions:
      aa['url'] = aa['url'].format(mid)
 
    table = InvoiceTable(Fee.objects.filter(member=M).order_by('-year'))
    RequestConfig(r, paginate={"per_page": 75}).configure(table)

    return render(r, template, {
			'title'		: title,
			'desc'		: desc,
			'actions'	: admin_actions,
       	            	'table'		: table,
                  })

  else: #error
    return render(r, done_template, {
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'],
		   })


# new invoice #
###############
@group_required('MEMBER')
def new_invoice(r, member_id):
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('members','/members/'),
                       	('invoices','/members/invoice/'),
               ) )
  M = Member.objects.get(id=member_id)
  generate_invoice(M)

  template = settings.TEMPLATE_CONTENT['profile']['newinv']['template']
  title = settings.TEMPLATE_CONTENT['profile']['newinv']['title'].format(id=M.id)
  message = settings.TEMPLATE_CONTENT['profile']['newinv']['message'].format(head=gen_fullname(M.head_of_list),year=date.today().strftime('%Y'))
  return render(r, template, {
			'title'		: title,
			'message'	: message,
	       })


# role_add #
############
@group_required('BOARD')
def role_add(r):
  r.breadcrumbs( ( ('board','/board/'),
                   ('members','/members/'),
                   ('add a role','/members/role/add/'),
                ) )

  if r.POST:
    rf = RoleForm(r.POST)
    if rf.is_valid():
      Rl = rf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['role']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['message'] + unicode(Rl),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['role']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in rf.errors]),
                })

  # no post yet -> empty form
  else:
    form = RoleForm()
    return render(r, settings.TEMPLATE_CONTENT['members']['role']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['role']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['role']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['role']['add']['submit'],
                'form': form,
                })


# NEW part #

# add user #
############
@group_required('BOARD')
def adduser(r,member_id):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('members','/members/'),
                       	(member_id+' details','/members/details/'+member_id),
               ) )
 
  M = Member.objects.get(pk=member_id)
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
	
      # gen attendance hashes for existing events
      for e in Event.objects.all():
        gen_attendance_hashes(e,Event.OTH,U)
      # and meetings
      for m in Meeting.objects.all():
        gen_attendance_hashes(m,Event.MEET,U)

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
@group_required('BOARD')
def make_head(r,member_id,user):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('members','/members/'),
                       	(member_id+' details','/members/details/'+member_id),
               ) )
 
  M = Member.objects.get(pk=member_id)
  old_H = M.head_of_list
  new_H = User.objects.get(username=user)

  #set new head-of-list
  M.head_of_list = new_H
  M.save()
  M.users.add(old_H) #add old head to users
  M.users.remove(new_H) #remove new head from users

  #set perms
  set_hol(new_H) #set perms for new head
  unset_hol(old_H) #remove perms for old head


  title = settings.TEMPLATE_CONTENT['profile']['make_head']['title'].format(id=M.id)
  template = settings.TEMPLATE_CONTENT['profile']['make_head']['template']
  message = settings.TEMPLATE_CONTENT['profile']['make_head']['message'].format(head=gen_fullname(M.head_of_list))

  return render(r,template, {
			'title'		: title,
			'message'	: message,
	       })



# make user the delegate #
##########################
@group_required('BOARD')
def make_delegate(r,member_id,user):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('members','/members/'),
                       	(member_id+' details','/members/details/'+member_id),
               ) )
 
  M = Member.objects.get(pk=member_id)
  old_D = M.delegate
  new_D = User.objects.get(username=user)

  #set new delegate
  M.delegate = new_D
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
@group_required('BOARD')
def moduser(r,member_id,user):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('members','/members/'),
                       	(member_id+' details','/members/details/'+member_id),
               ) )
 
  M = Member.objects.get(pk=member_id)
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
@group_required('BOARD')
def rmuser(r,member_id,user,really=False):
  r.breadcrumbs( (      
			('home','/home/'),
                       	('members','/members/'),
                       	(member_id+' details','/members/details/'+member_id),
               ) )
 
  M = Member.objects.get(pk=member_id)
  U = User.objects.get(username=user)

  title 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['title']
  template 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['template']
  message 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['message']

  done_title 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['done']['title']
  done_template 	= settings.TEMPLATE_CONTENT['profile']['rmuser']['done']['template']
  done_message 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['done']['message']

  error_title 		= settings.TEMPLATE_CONTENT['profile']['rmuser']['error']['title']
  error_message 	= settings.TEMPLATE_CONTENT['profile']['rmuser']['error']['message']

    
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

  #check if hol, del or admin
  # set hol, del list
  hd_list = (M.head_of_list.username, )
  try:
    hd_list.add(M.delegate.username)
  except:
    pass
  
  if r.user.username in hd_list or r.user.is_superuser :
    return render(r,template, {
			'title'		: title,
			'message'	: message.format(
								name	= gen_fullname(U),
								email	= U.email,
								login	= U.username,
								url	= '/members/'+M.pk+'/rmuser/'+U.username+'/REALLY/'
							),
		 })
  else: #error page
    return render(r,done_template, {
			'title'		: error_title,
                	'error_message'	: error_message,
		 })


