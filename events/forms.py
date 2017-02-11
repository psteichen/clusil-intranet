# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, FileField, CheckboxSelectMultiple, RadioSelect

from .models import Event, Distribution, Participant

#event form
class EventForm(ModelForm):
  message 	= CharField(widget=Textarea(attrs={'placeholder': "Message to add to the invitation.",}),required=True)
  attachement 	= FileField(required=False)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'agenda', 'deadline', 'message', 'attachement', )
    widgets = {
      'when'		: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'		: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'location'	: Textarea(attrs={'placeholder': "Provide full address details.",}),
      'agenda'		: Textarea(attrs={'placeholder': "Agenda or description of the event.",}),
      'deadline'	: TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }


#distribution form
class DistributionForm(ModelForm):

  class Meta:
    model = Distribution
    fields = ( 'partners', 'others', )
    widgets = {
      'partners'	: CheckboxSelectMultiple(),
      'others'		: Textarea(attrs={'placeholder': '''Please use following format (and only one entry per line): 
Firstname;Name;email'''}),
    }

#list events
class ListEventsForm(Form):
  events = ModelChoiceField(queryset=Event.objects.all())


#registration form
class RegistrationForm(ModelForm):

  class Meta:
    model = Participant
    fields = ( 'first_name', 'last_name', 'email', 'affiliation', )
    widgets = {
      'affiliation'	: RadioSelect(),
    }

