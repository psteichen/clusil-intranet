from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User

from members.models import Member
from members.groups.models import Group as WG

class MultiValueTextarea(forms.Textarea): 
  def render(self, name, value, attrs=None):
    if value is None: value = ''
    else: 
      out=''
      for f,l in value.values_list('first_name','last_name'):
        out += ' ' + f + ' ' + unicode.upper(l) + ' \n'
      #out = out.strip(';').strip() 

    final_attrs = self.build_attrs(attrs, name=name)

    from django.forms.util import flatatt
    from django.utils.html import conditional_escape
    from django.utils.encoding import force_unicode
    from django.utils.safestring import mark_safe

    return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                     conditional_escape(force_unicode(out))))

  
class MemberForm(forms.ModelForm):
  member_id = forms.CharField(label='Member-ID',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  member_type = forms.CharField(label='Membership-type',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  head_of_list = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  delegate = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  users = forms.CharField(label='Users:', widget=MultiValueTextarea(attrs={'readonly': 'readonly', 'class': 'readonly', 'cols': 25, 'rows': 8}))

  class Meta:
    model = Member
    exclude = ()

class MemberFormReadOnly(forms.ModelForm):
  member_id = forms.CharField(label='Member-ID',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  member_type = forms.CharField(label='Membership-type',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  firstname = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  lastname = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  organisation = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  address = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  postal_code = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  town = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  country = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  head_of_list = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  delegate = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  student_proof = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  class Meta:
    model = Member
    exclude = ( 'users', )

class ShortMemberFormReadOnly(forms.ModelForm):
  member_id = forms.CharField(label='Member-ID',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  member_type = forms.CharField(label='Membership-type',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  organisation = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  firstname = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  lastname = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))

  class Meta:
    model = Member
    fields = ( 'member_id', 'member_type', 'organisation', 'firstname', 'lastname', 'email', )

class WGFormCheckBox(forms.Form):
  wg = forms.ModelChoiceField(queryset=WG.objects.only('acronym').exclude(acronym='main').exclude(acronym='board').exclude(acronym__contains='leader').exclude(acronym="clusix"),widget=forms.CheckboxSelectMultiple(),label='Working Group',empty_label=None)

class WGFormRadio(forms.Form):
  wg = forms.ModelChoiceField(queryset=WG.objects.only('acronym').exclude(acronym='main').exclude(acronym='board').exclude(acronym__contains='leader').exclude(acronym="clusix"),widget=forms.RadioSelect(),label='Working Group',empty_label=None)

class UserCreationForm(UserCreationForm):

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', 'username',)

class UserChangeForm(UserChangeForm):
  username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'readonly'}))
  password = forms.CharField(label='Password',widget=forms.Textarea(attrs={'readonly': 'readonly', 'class': 'readonly', 'cols': 45, 'rows': 4}),initial='Raw passwords are not stored, so there is no way to see or change it here. But you can use the "change password for current user" form below to do so.')

  class Meta:
    model = User
    fields = ( 'username', 'password', 'first_name', 'last_name', 'email', )

class MemberUsersForm(forms.Form):
  users = forms.ModelChoiceField(queryset=User.objects.only('username').filter(username__in=Member.objects.only('users').values_list('users__username',flat=True)),widget=forms.CheckboxSelectMultiple(),label='Validate',empty_label=None)

class HolForm(forms.Form):
  head_of_list = forms.ModelChoiceField(queryset=User.objects.only('username').filter(username__in=Member.objects.only('users').values_list('users__username',flat=True)),widget=forms.RadioSelect(),label='Head of list',empty_label=None)
class DForm(forms.Form):
  delegate = forms.ModelChoiceField(queryset=User.objects.only('username').filter(username__in=Member.objects.only('users').values_list('users__username',flat=True)),widget=forms.RadioSelect(),label='Delegate',empty_label=None)
