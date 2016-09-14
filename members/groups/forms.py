
from django.forms import Form, ModelForm, TextInput, ModelChoiceField
from django.conf import settings

from .models import Group

#group form
class GroupForm(ModelForm):

  class Meta:
    model = Group
    fields = ( 'acronym', 'type', 'status', 'title', 'desc', ) 
