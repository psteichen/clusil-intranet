from django.conf.urls import patterns, url

from .forms import MemberTypeForm, AddressForm, RegisterUserForm, AffiliationForm, StudentProofForm, CaptchaForm
from .views import RegistrationWizard, show_delegate_form, show_student_proof_form


# registration wizard #
#forms
registration_forms = [
        ('type'		, MemberTypeForm),
        ('address'	, AddressForm),
        ('head'		, RegisterUserForm),
        ('delegate'	, RegisterUserForm),
        ('student_proof', StudentProofForm),
        ('group'	, AffiliationForm),
        ('captcha'	, CaptchaForm),
]
#condition dict
registration_condition_dict = {
	'delegate'	: show_delegate_form,
	'student_proof'	: show_student_proof_form,
}

#view
registration_wizard = RegistrationWizard.as_view(registration_forms, condition_dict=registration_condition_dict)


urlpatterns = patterns('',
  url(r'^$', registration_wizard, name='register'),
)
