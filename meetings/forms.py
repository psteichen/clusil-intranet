# coding=utf-8

from datetime import date

from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField
from django.conf import settings

from .models import Meeting, Location

#location form
class LocationForm(ModelForm):

  class Meta:
    model = Location
    fields = ( 'name', 'address', )
    widgets = {
      'address'         : Textarea(),
    }

#modify location wizard forms
class ListLocationsForm(Form):
  locations = ModelChoiceField(queryset=Location.objects.all())


#meeting form
class MeetingForm(ModelForm):
  additional_message = CharField(label='Message supplémentaire',widget=Textarea(attrs={'placeholder': "Message à transmettre dans l'inviation.",}),required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'additional_message', )
    widgets = {
      'title'	: TextInput(attrs={'readonly': 'readonly', }),
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
    }


#modify wizard forms
class ListMeetingsForm(Form):
  meetings = ModelChoiceField(queryset=Meeting.objects.all().order_by('when'))

class ModifyMeetingForm(ModelForm):

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
    }


