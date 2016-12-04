from django.db import models
from django.forms import Form, ModelForm, ModelChoiceField, CheckboxSelectMultiple, TextInput
from django.conf import settings

from members.models import Member

from .models import Fee

#class ManageReqForm(forms.Form):
#  reqs = forms.ModelChoiceField(queryset=Member.objects.only('member_id').filter(state=Member.REQ).order_by('member_id'),widget=forms.CheckboxSelectMultiple(),label='Validate',empty_label=None)

class FeeForm(Form):
  payments = ModelChoiceField(queryset=Member.objects.only('id').exclude(id__in=Fee.objects.filter(paid=True).values_list('member__id',flat=True)).order_by('id'),widget=CheckboxSelectMultiple(),label='Validate',empty_label=None)

class PaymentForm(ModelForm):

  class Meta:
    model = Fee
#    fields = ( 'member', 'invoice', 'year', 'paid_date', ) #maybe one day we could add thumbnail preview for invoice
    fields = ( 'member', 'year', 'paid_date', )
    widgets = {
      'paid_date'	: TextInput(attrs={'type': 'date', 'id': 'dpicker', }),
    }

