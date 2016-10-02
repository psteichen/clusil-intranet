from django.db import models
from django.forms import Form, ModelForm, ModelChoiceField, CheckboxSelectMultiple
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

from members.models import Member

from .models import Fee

#class ManageReqForm(forms.Form):
#  reqs = forms.ModelChoiceField(queryset=Member.objects.only('member_id').filter(state=Member.REQ).order_by('member_id'),widget=forms.CheckboxSelectMultiple(),label='Validate',empty_label=None)

class FeeForm(Form):
  payments = ModelChoiceField(queryset=Member.objects.only('id').exclude(id__in=Fee.objects.filter(paid=True).values_list('member__id',flat=True)).order_by('id'),widget=CheckboxSelectMultiple(),label='Validate',empty_label=None)

class PaymentForm(ModelForm):

  class Meta:
    model = Fee
    fields = ( 'member', 'invoice', 'year', 'paid_date', )

