from django.conf.urls import include, url
from django.contrib.auth.decorators import permission_required

from .forms import ListMembersForm, ModifyMemberForm, RoleForm
from .views import ModifyMemberWizard, show_role_form
from .views import list, renew, details, invoice, new_invoice
from .views import role_add
from .views import adduser, moduser, affiluser,  make_head, make_delegate, rmuser

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

urlpatterns = [
  url(r'^$', list, name='list'),

  url(r'^renew/$', renew, name='renew'),
  url(r'^modify/(?P<member_id>.+?)/$', modify_member_wrapper, name='modify'),
  url(r'^details/(?P<member_id>.+?)/$', details, name='details'),
  url(r'^invoice/new/(?P<member_id>.+?)/$', new_invoice, name='new_invoice'),
  url(r'^invoice/(?P<member_id>.+?)/$', invoice, name='invoice'),
  url(r'^adduser/(?P<member_id>.+?)/$', adduser, name='adduser'),

  url(r'^role/add/$', role_add, name='role_add'),

  url(r'^(?P<member_id>.+?)/moduser/(?P<user>.+?)/$', moduser, name='moduser'),
  url(r'^(?P<member_id>.+?)/affiluser/(?P<user>.+?)/$', affiluser, name='affiluser'),
  url(r'^(?P<member_id>.+?)/make_head/(?P<user>.+?)/$', make_head, name='make_head'),
  url(r'^(?P<member_id>.+?)/make_delegate/(?P<user>.+?)/$', make_delegate, name='make_delegate'),
  url(r'^(?P<member_id>.+?)/rmuser/(?P<user>.+?)/((?P<really>.+?)/)?$', rmuser, name='rmuser'),
]
