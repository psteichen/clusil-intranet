
from django.forms import Form, ModelForm, TextInput, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.conf import settings
from django.contrib.auth.models import User

from .models import Group

#group form
class GroupForm(ModelForm):

  class Meta:
    model = Group
    fields = ( 'acronym', 'type', 'status', 'title', 'desc', ) 

#adduser form
class AddUserForm(Form):
  users = ModelMultipleChoiceField(label='User',queryset=User.objects.all().order_by('last_name'),widget=CheckboxSelectMultiple())

