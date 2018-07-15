from django.conf.urls import url

from .forms import MemberTypeForm, AddressForm, RegisterUserForm, AffiliationForm, StudentProofForm, MultiUserFormSet, ErrorForm
from .views import RegistrationWizard, show_delegate_form, show_multi_user_form, show_student_proof_form, show_error_message

from .views import reg_home, validate


# registration wizard #
#forms
registration_forms = [
        ('type'		, MemberTypeForm),
        ('address'	, AddressForm),
        ('head'		, RegisterUserForm),
        ('delegate'	, RegisterUserForm),
        ('more'		, MultiUserFormSet),
        ('student_proof', StudentProofForm),
        ('error'	, ErrorForm),
#        ('captcha'	, CaptchaForm),
]
registration_forms_alt = [
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
	'error'		: show_error_message,
}
#view
registration_wizard = RegistrationWizard.as_view(registration_forms, condition_dict=registration_condition_dict)

registration_wizard_alt = RegistrationWizard.as_view(registration_forms_alt, condition_dict=registration_condition_dict)

urlpatterns = [
#  url(r'^$', registration_wizard, name='register'),
  url(r'^$', reg_home, name='register'),
  url(r'^validate/(?P<val_hash>.+?)/$', validate, name='validate'),
  url(r'^(?P<type>.+?)/$', registration_wizard_alt, name='register'),
]
