
from django.forms import Form, ModelForm, TextInput, ModelChoiceField
from django.conf import settings

from .models import Group

#group form
class GroupForm(ModelForm):

  class Meta:
    model = Group
    fields = ( 'type', 'title', 'desc', 'acronym', ) 

#modify forms
class ListGroupsForm(Form):
  groups = ModelChoiceField(label='Group',queryset=Group.objects.all().order_by('type'))

class ModifyGroupForm(ModelForm):

  class Meta:
    model = Group
    fields = ( 'acronym', 'type', 'status', 'title', 'desc',) 
    widgets = {
      'acronym'	: TextInput(attrs={'readonly':'readonly'})
    }
