from django.forms import  ModelForm, Form, CharField, Select, Textarea, ChoiceField, FileField, TextInput, ModelChoiceField, RadioSelect, CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User

from members.models import Member
from members.groups.models import Group as WG

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

class UserCreationForm(UserCreationForm):

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'email', )


#old stuff below
class MultiValueTextarea(Textarea): 
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

  
class MemberForm(ModelForm):
  member_id = CharField(label='Member-ID',widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  member_type = CharField(label='Membership-type',widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  head_of_list = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  delegate = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  users = CharField(label='Users:', widget=MultiValueTextarea(attrs={'readonly': 'readonly', 'class': 'readonly', 'cols': 25, 'rows': 8}))

  class Meta:
    model = Member
    exclude = ()

class MemberFormReadOnly(ModelForm):
  member_id = CharField(label='Member-ID',widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  member_type = CharField(label='Membership-type',widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  firstname = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  lastname = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  email = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  organisation = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  address = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  postal_code = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  town = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  country = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  head_of_list = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  delegate = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  student_proof = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  class Meta:
    model = Member
    exclude = ( 'users', )

class ShortMemberFormReadOnly(ModelForm):
  member_id = CharField(label='Member-ID',widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  member_type = CharField(label='Membership-type',widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  organisation = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  firstname = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  lastname = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))
  email = CharField(widget=TextInput(attrs={'readonly': 'readonly','class': 'readonly'}))

  class Meta:
    model = Member
    fields = ( 'member_id', 'member_type', 'organisation', 'firstname', 'lastname', 'email', )

class WGFormCheckBox(Form):
  wg = ModelChoiceField(queryset=WG.objects.only('acronym').exclude(acronym='main').exclude(acronym='board').exclude(acronym__contains='leader').exclude(acronym="clusix"),widget=CheckboxSelectMultiple(),label='Working Group',empty_label=None)

class WGFormRadio(Form):
  wg = ModelChoiceField(queryset=WG.objects.only('acronym').exclude(acronym='main').exclude(acronym='board').exclude(acronym__contains='leader').exclude(acronym="clusix"),widget=RadioSelect(),label='Working Group',empty_label=None)

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
