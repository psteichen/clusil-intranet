from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings

from django_tables2  import RequestConfig

from .functions import gen_group_initial
from .models import Group
from .forms import GroupForm
from .tables  import GroupTable


# index #
#########
@login_required
def index(r):
  r.breadcrumbs( ( ('home','/home/'),
                   ('members','/members/'),
                   ('groups','/members/groups/'),
               ) )

  return render(r, settings.TEMPLATE_CONTENT['groups']['template'], {
			'title': settings.TEMPLATE_CONTENT['groups']['title'],
                        'actions': settings.TEMPLATE_CONTENT['groups']['actions'],
               })

# add #
#######
@login_required
def add(r):
  r.breadcrumbs( ( ('home','/home/'),
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
#modify formwizard
class ModifyGroupWizard(SessionWizardView):

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(ModifyGroupWizard, self).get_context_data(form=form, **kwargs)

    #add breadcrumbs to context
    self.request.breadcrumbs( ( ('home','/home/'),
         	                ('members','/members/'),
	                        ('groups','/members/groups/'),
	               	        ('modify a group','/members/groups/modify/'),
                            ) )

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['groups']['modify']['title']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['groups']['modify'][self.steps.current]['title']})
      context.update({'next': settings.TEMPLATE_CONTENT['groups']['modify'][self.steps.current]['next']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(ModifyGroupWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'group':
      cleaned_data = self.get_cleaned_data_for_step('list') or {}
      if cleaned_data != {}:
        form.initial = gen_group_initial(cleaned_data['groups'])
        form.instance = Group.objects.get(pk=cleaned_data['groups'].pk)


    return form

  def done(self, fl, **kwargs):
    self.request.breadcrumbs( ( ('home','/home/'),
         	                ('members','/members/'),
	                        ('groups','/members/groups/'),
                	        ('modify a group','/members/groups/modify/'),
                            ) )

    template = settings.TEMPLATE_CONTENT['groups']['modify']['done']['template']

    G = None
    gf = fl[1]
    if gf.is_valid():
      G = gf.save()

    title = settings.TEMPLATE_CONTENT['groups']['modify']['done']['title'] % G.pk

    return render(self.request, template, {
				'title': title,
                 })

# list #
########
@login_required
def list(request):
  request.breadcrumbs( ( ('home','/home/'),
                         ('members','/members/'),
	                 ('groups','/members/groups/'),
                         ('list groups','/members/groups/list/'),
                        ) )

  table = GroupTable(Group.objects.all().order_by('type'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['groups']['list']['template'], {
                        'title': settings.TEMPLATE_CONTENT['groups']['list']['title'],
                        'desc': settings.TEMPLATE_CONTENT['groups']['list']['desc'],
                        'table': table,
                        })


