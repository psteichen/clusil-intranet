# coding=utf-8

from datetime import date

from django.conf import settings
from django.forms import Form, ModelForm, TextInput, Textarea, HiddenInput, CharField, ModelChoiceField, BooleanField, DateField, ModelMultipleChoiceField, CheckboxSelectMultiple, FileField, IntegerField
from django.forms.models import modelformset_factory, BaseModelFormSet

from members.functions import get_active_members

from .models import Meeting, Invitation

#meeting form
class MeetingForm(ModelForm):
  additional_message 	= CharField(label='Additional message',widget=Textarea(attrs={'placeholder': "Message to add to the invitation email.",}),required=False)
  attachement 		= FileField(required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'group', 'when', 'start', 'end', 'location', 'deadline', 'additional_message', 'attachement', )
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
  invitation = BooleanField(label='Adjust invitation message/attachement',required=False)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'start', 'end', 'location', 'deadline', 'invitation', )
    widgets = {
      'when'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
      'start'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'end'	: TextInput(attrs={'type': 'time', 'id': 'tpicker', }),
      'deadline': TextInput(attrs={'type': 'datetime', 'id': 'dtpicker', }),
    }

class ModifyInvitationForm(ModelForm):

  class Meta:
    model = Invitation
    fields = ( 'message', 'attachement', )
    widgets = {
      'message'	: Textarea(attrs={'placeholder': "Message to add to the invitation email.",}),
    }


#report form
class MeetingReportForm(Form):
  when		= CharField(label=u'Date',widget=TextInput(attrs={'readonly': 'readonly', }))
  report	= FileField(label='Minutes')
  send 		= BooleanField(label='Send invitations straight away!',required=False)

#delete form
class DeleteMeetingForm(Form):
  sure 		= BooleanField(label='Really sure?')
