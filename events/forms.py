# coding=utf-8

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField

from .models import Event

#event form
class EventForm(ModelForm):
  message 	= CharField(widget=Textarea(attrs={'placeholder': "Message to add to the invitation.",}),required=True)
  send 		= BooleanField(label='Send invitations straight away!',required=False)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'time', 'location', 'deadline', 'message', 'send', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
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

