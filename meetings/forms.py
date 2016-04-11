# coding=utf-8

from datetime import date

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, ModelMultipleChoiceField, CheckboxSelectMultiple, FileField, IntegerField
from django.forms.models import modelformset_factory, BaseModelFormSet

from members.functions import get_active_members

from .models import Meeting

#meeting form
class MeetingForm(ModelForm):
  additional_message 	= CharField(label='Additional message',widget=Textarea(attrs={'placeholder': "Message to add to the invitation email.",}),required=False)
  attachement 		= FileField(label='Annex(s)',required=False)
  send 			= BooleanField(label='Send invitations immediately',required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'group', 'when', 'time', 'location', 'deadline', 'additional_message', 'attachement', 'send', )
    widgets = {
#      'title'	: TextInput(attrs={'readonly': 'readonly', }),
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }


#modify wizard forms
class ListMeetingsForm(Form):
  meetings = ModelChoiceField(queryset=Meeting.objects.all().order_by('-num'))

class ModifyMeetingForm(ModelForm):
  attendance = BooleanField(label='Inscrire/excuser un membre',required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'time', 'location', 'deadline', 'attendance', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'time'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }


#report form
class MeetingReportForm(Form):
  title		= CharField(label=u'Titre',widget=TextInput(attrs={'readonly': 'readonly', }))
  when		= CharField(label=u'Date',widget=TextInput(attrs={'readonly': 'readonly', }))
  report	= FileField(label='Compte rendu')
  send 		= BooleanField(label='Envoi du compte rendu aux membres',required=False)

