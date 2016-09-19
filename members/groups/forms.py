
from django.forms import Form, ModelForm, TextInput, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.conf import settings
from django.contrib.auth.models import User

from .models import Group, Affiliation

#group form
class GroupForm(ModelForm):

  class Meta:
    model = Group
    fields = ( 'acronym', 'type', 'status', 'title', 'desc', ) 

#adduser form
class AddUserForm(Form):
  def __init__(self,*args,**kwargs):
    self.gid = kwargs.pop('gid')
    super(AddUserForm,self).__init__(*args,**kwargs)
    self.fields['users'].queryset = User.objects.exclude(pk__in=Affiliation.objects.filter(group=self.gid).values('user_id'))
  
  users = ModelMultipleChoiceField(label='User',queryset=User.objects.all(),widget=CheckboxSelectMultiple())

