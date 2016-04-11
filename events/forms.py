# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField

from .models import Event

#event form
class EventForm(ModelForm):
  additional_message 	= CharField(label='Message supplémentaire',widget=Textarea(attrs={'placeholder': "Message à transmettre dans l'invitation.",}),required=False)
  send 			= BooleanField(label='Envoi direct des invitations',required=False)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'deadline', 'additional_message', 'send', )
    widgets = {
#      'title'	: TextInput(attrs={'readonly': 'readonly', }),
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
      'deadline': TextInput(attrs={'type': 'date', }),
    }


#modify wizard forms
class ListEventsForm(Form):
  events = ModelChoiceField(queryset=Event.objects.all())

class ModifyEventForm(ModelForm):
  attendance = BooleanField(label='Inscrire/excuser un membre')

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'deadline', 'attendance',  )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', }),
      'time'	: TextInput(attrs={'type': 'time', }),
      'deadline': TextInput(attrs={'type': 'date', }),
    }

