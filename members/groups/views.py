from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.forms.models import model_to_dict

from django_tables2  import RequestConfig

from .functions import gen_group_initial
from .models import Group, Affiliation
from .forms import GroupForm
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

  return render(request, settings.TEMPLATE_CONTENT['groups']['affil']['template'], {
                        'title': settings.TEMPLATE_CONTENT['groups']['affil']['title'].format(group),
                        'overview': overview,
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
                'title': settings.TEMPLATE_CONTENT['groups']['add']['done']['title'], 
                'message': settings.TEMPLATE_CONTENT['groups']['add']['done']['message'] + unicode(G),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['groups']['add']['done']['template'], {
                'title': settings.TEMPLATE_CONTENT['groups']['add']['done']['title'], 
                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in gf.errors]),
                })

  # no post yet -> empty form
  else:
    form = GroupForm()
    return render(r, settings.TEMPLATE_CONTENT['groups']['add']['template'], {
                'title': settings.TEMPLATE_CONTENT['groups']['add']['title'],
                'desc': settings.TEMPLATE_CONTENT['groups']['add']['desc'],
                'submit': settings.TEMPLATE_CONTENT['groups']['add']['submit'],
                'form': form,
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
                	'title': settings.TEMPLATE_CONTENT['groups']['modify']['done']['title'], 
        	        'message': settings.TEMPLATE_CONTENT['groups']['modify']['done']['message'] + unicode(G),
                })

    # form not valid -> error
    else:
      return render(r, settings.TEMPLATE_CONTENT['groups']['modify']['done']['template'], {
        	        'title': settings.TEMPLATE_CONTENT['groups']['modify']['done']['title'], 
	                'error_message': settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in gf.errors]),
                })

  # no post yet -> empty form
  else:
    form = GroupForm(initial=model_to_dict(Group.objects.get(pk=group)))
    return render(r, settings.TEMPLATE_CONTENT['groups']['modify']['template'], {
			'title': settings.TEMPLATE_CONTENT['groups']['modify']['title'],
	                'desc': settings.TEMPLATE_CONTENT['groups']['modify']['desc'],
        	        'submit': settings.TEMPLATE_CONTENT['groups']['modify']['submit'],
	                'form': form,
                })


