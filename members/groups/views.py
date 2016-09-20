from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.forms.models import model_to_dict

from django_tables2  import RequestConfig

from .functions import gen_group_initial
from .models import Group, Affiliation
from .forms import GroupForm, AddUserForm
from .tables  import GroupTable


# list #
#########
@permission_required('cms.SECR')
def list(request):
  request.breadcrumbs( ( 
				('board','/board/'),
                         	('members','/members/'),
                         	('groups','/members/groups/'),
                     ) )

  table = GroupTable(Group.objects.all())
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['groups']['template'], {
                        'title': settings.TEMPLATE_CONTENT['groups']['title'],
                        'desc': settings.TEMPLATE_CONTENT['groups']['desc'],
                        'actions': settings.TEMPLATE_CONTENT['groups']['actions'],
                        'table': table,
                        })


# affil #
#########
@permission_required('cms.SECR')
def affil(request,group):
  request.breadcrumbs( ( 
				('board','/board/'),
                         	('members','/members/'),
                         	('groups','/members/groups/'),
                         	(group+' affiliates','/members/groups/affil/'+group+'/'),
                     ) )

  A = Affiliation.objects.filter(group=group)

  overview = render_to_string(settings.TEMPLATE_CONTENT['groups']['affil']['overview']['template'], { 
					'affil'	: A, 
			     })
  actions = settings.TEMPLATE_CONTENT['groups']['affil']['actions']
  for a in actions:
    a['url'] = a['url'].format(group)

  return render(request, settings.TEMPLATE_CONTENT['groups']['affil']['template'], {
                        'title'		: settings.TEMPLATE_CONTENT['groups']['affil']['title'].format(group),
                        'actions'	: actions,
                        'overview'	: overview,
               })


# add #
#######
@permission_required('cms.SECR')
def add(r):
  r.breadcrumbs( ( 
			('home','/home/'),
                   	('members','/members/'),
                   	('groups','/members/groups/'),
                   	('add a group','/members/groups/add/'),
               ) )

  if r.POST:
    gf = GroupForm(r.POST)
    if gf.is_valid():
      G = gf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['groups']['add']['done']['template'], {
                'title'		: settings.TEMPLATE_CONTENT['groups']['add']['done']['title'], 
                'message'	: settings.TEMPLATE_CONTENT['groups']['add']['done']['message'] + unicode(G),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['groups']['add']['done']['template'], {
                'title'		: settings.TEMPLATE_CONTENT['groups']['add']['done']['title'], 
                'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in gf.errors]),
                })

  # no post yet -> empty form
  else:
    form = GroupForm()
    return render(r, settings.TEMPLATE_CONTENT['groups']['add']['template'], {
                'title'		: settings.TEMPLATE_CONTENT['groups']['add']['title'],
                'desc'		: settings.TEMPLATE_CONTENT['groups']['add']['desc'],
                'submit'	: settings.TEMPLATE_CONTENT['groups']['add']['submit'],
                'form'		: form,
                })

# modify #
##########
def modify(r,group):
  r.breadcrumbs( ( 
			('home','/home/'),
       	                ('members','/members/'),
                        ('groups','/members/groups/'),
               	        ('modify a group','/members/groups/modify/'),
               ) )

  template = settings.TEMPLATE_CONTENT['groups']['modify']['done']['template']

  if r.POST:
    gf = GroupForm(r.POST)
    if gf.is_valid():
      G = gf.save()
      
      # all fine -> done
      return render(r, settings.TEMPLATE_CONTENT['groups']['modify']['done']['template'], {
                	'title'		: settings.TEMPLATE_CONTENT['groups']['modify']['done']['title'] % unicode(G), 
        	        'message'	: settings.TEMPLATE_CONTENT['groups']['modify']['done']['message'] + unicode(G),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['groups']['modify']['done']['template'], {
        	        'title'		: settings.TEMPLATE_CONTENT['groups']['modify']['done']['title'] % unicode(G), 
	                'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in gf.errors]),
                })

  # no post yet -> empty form
  else:
    form = GroupForm(initial=model_to_dict(Group.objects.get(pk=group)))
    return render(r, settings.TEMPLATE_CONTENT['groups']['modify']['template'], {
			'title'		: settings.TEMPLATE_CONTENT['groups']['modify']['title'],
	                'desc'		: settings.TEMPLATE_CONTENT['groups']['modify']['desc'],
        	        'submit'	: settings.TEMPLATE_CONTENT['groups']['modify']['submit'],
	                'form'		: form,
                })


# adduser #
###########
@permission_required('cms.SECR')
def adduser(r,group):
  r.breadcrumbs( ( 
			('board','/board/'),
                      	('members','/members/'),
                       	('groups','/members/groups/'),
                       	(group+' affiliates','/members/groups/affil/'+group+'/'),
               ) )

  template 	= settings.TEMPLATE_CONTENT['groups']['adduser']['template']
  title		= settings.TEMPLATE_CONTENT['groups']['adduser']['title']
  desc		= settings.TEMPLATE_CONTENT['groups']['adduser']['desc']
  submit	= settings.TEMPLATE_CONTENT['groups']['adduser']['submit']

  done_template = settings.TEMPLATE_CONTENT['groups']['adduser']['done']['template']
  done_title	= settings.TEMPLATE_CONTENT['groups']['adduser']['done']['title'] 

  if r.POST:
    auf = AddUserForm(r.POST,gid=group)
    if auf.is_valid():
      users = auf.cleaned_data['users']
      for u in users:
        Affiliation.objects.create(group=Group.objects.get(pk=group),user=u)
      
      # all fine -> done
      return render(r, done_template, {
                	'title'		: done_title.format(group), 
                	'list'		: users, 
                })

    # form not valid -> error
    else:
      return render(r, done_template, {
        	        'title'		: done_title, 
	                'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in auf.errors]),
                })

  # no post yet -> empty form
  else:
#    form = AddUserForm(Affiliation.objects.filter(group=group).only('user').values())
    form = AddUserForm(gid=group)
    return render(r, template, {
			'title'		: title.format(group),
	                'desc'		: desc,
        	        'submit'	: submit,
	                'form'		: form,
                })

