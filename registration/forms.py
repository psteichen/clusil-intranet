# coding=utf-8

from captcha.fields import ReCaptchaField

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, ChoiceField, ModelForm, CharField, FileField,  ModelMultipleChoiceField, CheckboxSelectMultiple, TextInput, FileField, EmailField, BooleanField

from members.models import Member, Address
from members.groups.models import Group, Affiliation


class MemberTypeForm(Form):
  member_type = ChoiceField(label='Membership type',choices=Member.MEMBER_TYPES)

class AddressForm(ModelForm):
  organisation 	= CharField(required=False)
  first_name 	= CharField(required=False)
  last_name 	= CharField(required=False)
  email 	= EmailField(required=False)

  class Meta:
    model = Address
    fields = ( 'first_name', 'last_name', 'email', 'organisation', 'street', 'num', 'postal_code', 'town', 'country', )

class RegisterUserForm(UserCreationForm):
  delegate 	= BooleanField(label='add Delegate?',required=False)
  class Meta:
    model = User
    fields = ( 'first_name', 'last_name', 'email', 'username', 'password1', 'password2', )
    widgets = {
      'email'		: TextInput(attrs={'type': 'email', }),
      'password1'	: TextInput(attrs={'type': 'password', }),
      'password2'	: TextInput(attrs={'type': 'password', }),
    }

class StudentProofForm(Form):
  class Meta:
    model = Member
    fields = ( 'student_proof', )

class AffiliationForm(Form):
  groups 	= ModelMultipleChoiceField(
			queryset=Group.objects.only('acronym','title').exclude(acronym='default').exclude(acronym='board').exclude(acronym__contains='leader').exclude(acronym='clusix'),
			widget=CheckboxSelectMultiple(),
			label='Select Group affiliations',
		  )

class CaptchaForm(Form):
  captcha = ReCaptchaField(attrs={'theme' : 'clean'})

