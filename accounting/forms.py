from django.db import models
from django.forms import Form, ModelChoiceField, CheckboxSelectMultiple
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

from members.models import Member

from .models import Fee

#class ManageReqForm(forms.Form):
#  reqs = forms.ModelChoiceField(queryset=Member.objects.only('member_id').filter(state=Member.REQ).order_by('member_id'),widget=forms.CheckboxSelectMultiple(),label='Validate',empty_label=None)

class FeeForm(Form):
  payments = ModelChoiceField(queryset=Member.objects.only('id').exclude(id__in=Fee.objects.filter(paid=True).values_list('member__id',flat=True)).order_by('id'),widget=CheckboxSelectMultiple(),label='Validate',empty_label=None)

#class ManageAffilForm(forms.Form):
#  member = forms.ModelChoiceField(queryset=Member.objects.filter(state=Member.MEM).order_by('member_id'))
#  committee = forms.ModelMultipleChoiceField(queryset=Committee.objects.all(),widget=forms.CheckboxSelectMultiple)

#class ManageAffilForm(forms.Form):
#  def __init__(self, *args, **kwargs):
#    super(ManageAffilForm, self).__init__(*args, **kwargs)
#    self.fields['Cs'] = forms.ModelMultipleChoiceField(queryset=Committee.objects.only('short','desc'),widget=forms.CheckboxSelectMultiple(),label='Committees')
#
#  mem = forms.ModelChoiceField(queryset=Member.objects.only('member_id').filter(state=Member.MEM).exclude(member_id__in=Fee.objects.filter(payed=False).values_list('member__member_id',flat=True)),label='Member',widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'readonly'}),empty_label=None)
#
#  mem = forms.CharField(label='Member-ID:',widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'readonly'}))
#  committee = forms.ModelMultipleChoiceField(queryset=Committee.objects.all(),widget=forms.CheckboxSelectMultiple(),label='Committees',empty_label=None)

