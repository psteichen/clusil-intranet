from datetime import date
from random import random

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.contrib.auth.models import User

from django_tables2  import RequestConfig

from cms.functions import show_form, notify_by_email

from registration.functions import gen_hash

from accounting.models import Fee
from accounting.functions import generate_invoice

from .profile.tables import InvoiceTable

from .functions import gen_member_initial, gen_role_initial, gen_fullname, gen_member_overview, get_active_members, gen_renewal_link, gen_member_fullname, user_in_board
from .models import Member, Role, Renew
from .forms import MemberForm, RoleForm
from .tables  import MemberTable


###############
# BOARD views #
###############

# list #
#########
@permission_required('cms.SECR')
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
@permission_required('cms.SECR')
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
    salt2=float(year)*random()
    renew_hash_code = gen_hash(settings.RENEW_SALT,unicode(m.head_of_list.email)+unicode(m.address).encode('ascii', 'ignore'),15,salt2)
    # build request mail
    message_content = {
        'FULLNAME'	: gen_member_fullname(m),
        'YEAR'		: year,
	'LINK'		: gen_renewal_link(renew_hash_code),
    }
    # send confirmation
    ok=notify_by_email(m.head_of_list.email,email_title,message_content,email_template)
    if not ok:
      return render(r, error_template, { 
				'mode': 'Error in email request', 
				'message': settings.TEMPLATE_CONTENT['error']['email'],
		   })

    try:
      renew = Renew(member=m,year=year,renew_code=renew_hash_code)
      renew.save()
    except:
      renew = Renew.objects.get(member=m,year=year)
      renew.renew_code = renew_hash_code
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
@login_required
def details(r, member_id):
  member = Member.objects.get(id=member_id)

  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('details of member: '+unicode(member_id),'/members/details/'+member_id+'/'),
               ) )

  if r.user == member.head_of_list or r.user == member.delegate:
#  if r.user == member.head_of_list or r.user == member.delegate or user_in_board(r.user):
    message = gen_member_overview(settings.TEMPLATE_CONTENT['members']['details']['overview']['template'],member,settings.TEMPLATE_CONTENT['members']['details']['overview']['actions'])
  elif user_in_board(r.user):
    actions = settings.TEMPLATE_CONTENT['members']['details']['overview']['admin_actions']
    for a in actions:
      a['url'] = a['url'].format(member_id)

    message = gen_member_overview(settings.TEMPLATE_CONTENT['members']['details']['overview']['template'],member,actions)
  else:
    message = gen_member_overview(settings.TEMPLATE_CONTENT['members']['details']['readonly']['template'],member)
  

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
@permission_required('cms.MEMBER')
def invoice(r, member_id):
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('members','/members/'),
                       	('invoices','/members/invoice/'),
               ) )
  M = Member.objects.get(id=member_id)

  template = settings.TEMPLATE_CONTENT['profile']['invoice']['template']
  done_template = settings.TEMPLATE_CONTENT['profile']['invoice']['done']['template']
  if M != None:  
    title = settings.TEMPLATE_CONTENT['profile']['invoice']['title'] % { 'member' : M.id, }
    desc = settings.TEMPLATE_CONTENT['profile']['invoice']['desc']
    actions = settings.TEMPLATE_CONTENT['profile']['invoice']['admin_actions']
    for a in actions:
      a['url'] = a['url'].format(member_id)
 
    table = InvoiceTable(Fee.objects.filter(member=M).order_by('-year'))
    RequestConfig(r, paginate={"per_page": 75}).configure(table)

    return render(r, template, {
			'title'		: title,
			'desc'		: desc,
			'actions'	: actions,
       	            	'table'		: table,
                  })

  else: #error
    return render(r, done_template, {
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'],
		   })


# new invoice #
###############
@permission_required('cms.MEMBER')
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
@permission_required('cms.BOARD')
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


