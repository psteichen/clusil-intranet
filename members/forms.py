from datetime import date

from django.forms import Form, ModelForm, TextInput, Textarea, ModelChoiceField, BooleanField
from django.conf import settings

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

