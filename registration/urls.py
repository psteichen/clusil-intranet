from django.conf.urls import patterns, url

from .forms import MemberTypeForm, AddressForm, RegisterUserForm, AffiliationForm, StudentProofForm, MultiUserFormSet
from .views import RegistrationWizard, show_delegate_form, show_multi_user_form, show_student_proof_form

from .views import validate


# registration wizard #
#forms
registration_forms = [
        ('type'		, MemberTypeForm),
        ('address'	, AddressForm),
        ('head'		, RegisterUserForm),
        ('delegate'	, RegisterUserForm),
        ('more'		, MultiUserFormSet),
        ('student_proof', StudentProofForm),
#        ('group'	, AffiliationForm),
#        ('captcha'	, CaptchaForm),
]
registration_forms_alt = [
        ('address'	, AddressForm),
        ('head'		, RegisterUserForm),
        ('delegate'	, RegisterUserForm),
        ('more'		, MultiUserFormSet),
        ('student_proof', StudentProofForm),
#        ('group'	, AffiliationForm),
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

registration_wizard_alt = RegistrationWizard.as_view(registration_forms_alt, condition_dict=registration_condition_dict)

urlpatterns = patterns('',
  url(r'^$', registration_wizard, name='register'),
  url(r'^(?P<type>.+?)/$', registration_wizard_alt, name='register'),
  url(r'^validate/(?P<val_hash>.+?)/$', validate, name='validate'),
)
