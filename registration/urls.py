from django.conf.urls import url
from django.views.generic.base import RedirectView


from .forms import MemberTypeForm, AddressForm, RegisterUserForm, StudentProofForm, MultiUserFormSet, ErrorForm
from .views import RegistrationWizard, show_delegate_form, show_multi_user_form, show_student_proof_form

from .views import validate


# registration wizard #
#forms
registration_forms = [
        ('address'	, AddressForm),
        ('head'		, RegisterUserForm),
        ('delegate'	, RegisterUserForm),
        ('more'		, MultiUserFormSet),
        ('student_proof', StudentProofForm),
#        ('captcha'	, CaptchaForm),
]
#condition dict
registration_condition_dict = {
	'delegate'	: show_delegate_form,
        'more'		: show_multi_user_form,
	'student_proof'	: show_student_proof_form,
}
#view
registration_wizard = RegistrationWizard.as_view(registration_forms, condition_dict=registration_condition_dict)

urlpatterns = [
  url(r'^$', RedirectView.as_view(url='/'), name='redirect'),
  url(r'^validate/(?P<val_hash>.+?)/$', validate, name='validate'),
  url(r'^(?P<type>.+?)/$', registration_wizard, name='register'),
]
