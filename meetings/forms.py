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
  attachement 		= FileField(required=False)
  send 			= BooleanField(label='Send invitations straight away!',required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'group', 'when', 'start', 'end', 'location', 'deadline', 'additional_message', 'attachement', 'send', )
    labels = {
      'title'	: 'Meeting Topic/Title',
    }
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'start'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'end'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'location': Textarea(attrs={'placeholder': "Provide full address details.",}),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }


#modify wizard forms
class ListMeetingsForm(Form):
  meetings = ModelChoiceField(queryset=Meeting.objects.all().order_by('-num'))

class ModifyMeetingForm(ModelForm):
#not used yet  attendance = BooleanField(label='Subscribe/excuse a membre',required=False)

  class Meta:
    model = Meeting
#    fields = ( 'title', 'when', 'start', 'end', 'location', 'deadline', 'attendance', )
    fields = ( 'title', 'when', 'start', 'end', 'location', 'deadline', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'start'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'end'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }


#report form
class MeetingReportForm(Form):
  when		= CharField(label=u'Date',widget=TextInput(attrs={'readonly': 'readonly', }))
  report	= FileField(label='Minutes')
  send 		= BooleanField(label='Send invitations straight away!',required=False)
