from datetime import date

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, ReadOnlyPasswordHashField
from django.forms import  ModelForm, Form, CharField, Select, Textarea, ChoiceField, FileField, TextInput, ModelChoiceField, ModelMultipleChoiceField, RadioSelect, CheckboxSelectMultiple, BooleanField

from .models import Member, Role

#role form
class RoleForm(ModelForm):

  class Meta:
    model = Role
    fields = ( 'title', 'user', 'group', 'start_date', 'end_date', ) 
    widgets = {
      'start_date'	: TextInput(attrs={'type': 'date', }),
      'end_date'	: TextInput(attrs={'type': 'date', }),
    }


#member form
class MemberForm(ModelForm):

  class Meta:
    model = Member
    fields = ( 'address', 'head_of_list', 'delegate', ) 
    widgets = {
      'address'		: Textarea(attrs={'cols': 20, 'rows': 5, }),
    }


#modify forms
class ListMembersForm(Form):
  members = ModelChoiceField(label='Member',queryset=Member.objects.all().order_by('id'))

class ModifyMemberForm(MemberForm):
  role = BooleanField(label='Modify role:',required=False)



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
