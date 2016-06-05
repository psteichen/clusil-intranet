from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import permission_required

from .forms import ListMembersForm, ModifyMemberForm, RoleForm
from .views import ModifyMemberWizard, show_role_form
from .views import list, details
from .views import role_add

# modify wizard #
#forms
modify_member_forms = [
        ('member'       , ModifyMemberForm),
        ('role'         , RoleForm),
]
#condition dict
modify_member_condition_dict = {
	'role'		: show_role_form,
}

#view
modify_member_wizard = ModifyMemberWizard.as_view(modify_member_forms, condition_dict=modify_member_condition_dict)
#wrapper with specific permissions
modify_member_wrapper = permission_required('cms.SECR')(modify_member_wizard)

urlpatterns = patterns('',
  url(r'^$', list, name='list'),

  url(r'^modify/(?P<member_id>.+?)/$', modify_member_wrapper, name='modify'),
  url(r'^details/(?P<member_id>.+?)/$', details, name='details'),

  url(r'^role/add/$', role_add, name='role_add'),
)
