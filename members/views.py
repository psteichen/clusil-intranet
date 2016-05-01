from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.contrib.auth.models import User

from django_tables2  import RequestConfig

from cms.functions import show_form

from .functions import gen_member_initial, gen_role_initial, gen_fullname, gen_member_overview
from .models import Member, Role
from .forms import MemberForm, RoleForm
from .tables  import MemberTable


###############
# BOARD views #
###############

# list #
#########
@permission_required('cms.BOARD')
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


# add #
#######
@permission_required('cms.BOARD')
def add(r):
  r.breadcrumbs( ( ('board','/board/'),
                   ('members','/members/'),
                   ('add a member','/members/add/'),
                ) )

  if r.POST:
    mf = MemberForm(r.POST)
    if mf.is_valid():
      Me = mf.save(commit=False)
      Me.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'message': '',
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['members']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in mf.errors]),
                })
  # no post yet -> empty form
  else:
    form = MemberForm()
    return render(r, settings.TEMPLATE_CONTENT['members']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['members']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['members']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['members']['add']['submit'],
                'form': form,
                })

# details #
###########
@login_required
def details(r, member_id):
  member = Member.objects.get(id=member_id)

  r.breadcrumbs( ( 
			('home','/'),
                   	('members','/members/'),
                   	('details of member: '+unicode(member),'/members/list/'+member_id+'/'),
               ) )

  title = settings.TEMPLATE_CONTENT['members']['details']['title'] % { 'member' : unicode(member), }
  message = gen_member_overview(settings.TEMPLATE_CONTENT['members']['details']['overview']['template'],member)

  return render(r, settings.TEMPLATE_CONTENT['members']['details']['template'], {
                   'title': title,
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
    list_data = self.get_cleaned_data_for_step('list') or {}
    if list_data != {}:
      M = Member.objects.get(pk=list_data['members'].id)
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
    if step != 'list':
      list_data = self.get_cleaned_data_for_step('list') or {}
      if list_data != {}:
        M = Member.objects.get(pk=list_data['members'].id)
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

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( ( ('home','/home/'),
         	                ('member','/members/'),
                	        ('modify a member','/members/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['members']['modify']['done']['template']

    M = R = None
    mf = fl[1]
    role = mf.cleaned_data['role']
    if role: rf = fl[2]

    if mf.is_valid():
      M = mf.save()

    if role: 
      if rf.is_valid():
        R = rf.save()

    title = settings.TEMPLATE_CONTENT['members']['modify']['done']['title'] % M

    return render(self.request, template, {
				'title': title,
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


