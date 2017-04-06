from django.forms import  ModelForm, Form, CharField, Select, Textarea, ChoiceField, FileField, TextInput, ModelChoiceField, ModelMultipleChoiceField, RadioSelect, CheckboxSelectMultiple, HiddenInput
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User

from members.models import Member
from members.groups.models import Group

#member profile form for modify view
class ProfileForm(Form):
  orga 		= CharField(label='Organisation',required=False)
  fn		= CharField(label='Firstname',required=False)
  ln 		= CharField(label='Lastname',required=False)
  email 	= CharField(label='Email',required=False)
  street 	= CharField(label='Address (street)',required=False)
  pc		= CharField(label='Address (postal code)',required=False)
  town		= CharField(label='Address (town)',required=False)
  country	= CharField(label='Address (country)',required=False)
  sp		= FileField(label='Student proof',required=False)

class UserForm(ModelForm):

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', )

  
def gen_choices(ty):
  choices=[]
  Gs = None
  if ty == 'wg': Gs = Group.objects.filter(type=Group.WG).filter(status=Group.ACT)
  if ty == 'ag': Gs = Group.objects.filter(type=Group.AG).filter(status=Group.ACT)
  if ty == 'tl': Gs = Group.objects.filter(type=Group.TL).filter(status=Group.ACT)
  i=0
  for g in Gs:
    choices.append((g,unicode(g)))
    i+=1

  return tuple(choices)
  
  
class AffiliateForm(Form):
  wgs = ModelMultipleChoiceField(
		queryset=Group.objects.filter(type=Group.WG).filter(status=Group.ACT),
		widget=CheckboxSelectMultiple(),
		label='Working Groups',
		required=False
	)
#  wgs = ChoiceField(
#		choices=gen_choices('wg'),
#		widget=CheckboxSelectMultiple(),
#		label='Working Groups',
#		required=False
#	)
  ags = ModelMultipleChoiceField(
		queryset=Group.objects.filter(type=Group.AG).filter(status=Group.ACT),
		widget=CheckboxSelectMultiple(),
		label='Ad-hoc Groups',
		required=False
	)
  tls = ModelMultipleChoiceField(
		queryset=Group.objects.filter(type=Group.TL).filter(status=Group.ACT),
		widget=CheckboxSelectMultiple(),
		label='Tools',
		required=False
	)



class UserChangeForm(UserChangeForm):
  username = CharField(label='Username',widget=TextInput(attrs={'readonly': 'readonly', 'class': 'readonly'}))
  password = CharField(label='Password',widget=Textarea(attrs={'readonly': 'readonly', 'class': 'readonly', 'cols': 45, 'rows': 4}),initial='Raw passwords are not stored, so there is no way to see or change it here. But you can use the "change password for current user" form below to do so.')

  class Meta:
    model = User
    fields = ( 'username', 'password', 'first_name', 'last_name', 'email', )

class MemberUsersForm(Form):
  users = ModelChoiceField(queryset=User.objects.only('username').filter(username__in=Member.objects.only('users').values_list('users__username',flat=True)),widget=CheckboxSelectMultiple(),label='Validate',empty_label=None)

class HolForm(Form):
  head_of_list = ModelChoiceField(queryset=User.objects.only('username').filter(username__in=Member.objects.only('users').values_list('users__username',flat=True)),widget=RadioSelect(),label='Head of list',empty_label=None)
class DForm(Form):
  delegate = ModelChoiceField(queryset=User.objects.only('username').filter(username__in=Member.objects.only('users').values_list('users__username',flat=True)),widget=RadioSelect(),label='Delegate',empty_label=None)


class StudentProofForm(Form):
  code 		= CharField(widget=HiddenInput())
  member 	=  CharField(widget=HiddenInput())
  student_proof	= FileField(label='Student proof',required=False)

