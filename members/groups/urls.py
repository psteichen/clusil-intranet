from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from .forms import ListGroupsForm, ModifyGroupForm
from .views import ModifyGroupWizard
from .views import index, add, list

# modify wizard #
#forms
modify_group_forms = [
        ('list'         , ListGroupsForm),
        ('group'	, ModifyGroupForm),
]

#view
modify_group_wizard = ModifyGroupWizard.as_view(modify_group_forms)
#wrapper with specific permissions
modify_group_wrapper = login_required(modify_group_wizard)

urlpatterns = patterns('',
  url(r'^$', index, name='index'),

  url(r'^add/', add, name='add'),
  url(r'^modify/', modify_group_wrapper, name='modify'),
  url(r'^list/', list, name='list'),
)
