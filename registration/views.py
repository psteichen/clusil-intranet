# -*- coding: utf-8 -*-
from datetime import date

from django.conf import settings
from django.shortcuts import render 
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import Permission

from intranet.functions import show_form, notify_by_email

from accounting.functions import generate_invoice
from members.models import Member, Organisation, Address
from members.groups.models import Group, Affiliation

from .functions import gen_member_id, add_to_groups, gen_fullname

def show_delegate_form(wizard):
  return show_form(wizard,'type','member_type',Member.ORG) and show_form(wizard,'head','delegate',True)

def show_student_proof_form(wizard):
  return show_form(wizard,'type','member_type',Member.STD)

# registration formwizard #
###########################
class RegistrationWizard(SessionWizardView):
  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(RegistrationWizard, self).get_context_data(form=form, **kwargs)

    if self.steps.current != None:
      context.update({'title': settings.TEMPLATE_CONTENT['reg']['register']['title']})
      context.update({'step_title': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['title']})
      context.update({'step_desc': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['desc']})
      context.update({'first': settings.TEMPLATE_CONTENT['reg']['register']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['reg']['register']['prev']})
      context.update({'next': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['next']})

    if self.steps.current == 'head':
      cleaned_data = self.get_cleaned_data_for_step('type') or {}
      if int(cleaned_data['member_type']) != Member.ORG:
        context.update({'step_title': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['alttitle']})
        context.update({'step_desc': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['altdesc']})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(RegistrationWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'address':
      cleaned_data = self.get_cleaned_data_for_step('type') or False
      if cleaned_data:
        ty = int(cleaned_data['member_type'])
        if ty == Member.ORG:
          del form.fields['first_name']
          del form.fields['last_name']
          del form.fields['email']
        if ty == Member.IND:
          del form.fields['organisation']
        if ty == Member.STD:
          del form.fields['organisation']

    if step == 'head':
      cleaned_data = self.get_cleaned_data_for_step('address') or False
      if cleaned_data:
        try:
          form.fields['first_name'].initial = cleaned_data['first_name']
        except: pass
        try:
          form.fields['last_name'].initial = cleaned_data['last_name']
        except: pass
        try:
          form.fields['email'].initial = cleaned_data['email']
        except: pass

    if step == 'delegate':
      del form.fields['delegate']

    return form

  def done(self, fl, form_dict, **kwargs):

    template = settings.TEMPLATE_CONTENT['reg']['register']['done']['template']
    e_template = settings.TEMPLATE_CONTENT['reg']['register']['done']['email_template']

    m_id = gen_member_id()

    M = O = A = U = D = Gs = None

    t_f = form_dict['type']
    ty = int(t_f.cleaned_data['member_type'])
    a_f = form_dict['address']
    h_f = form_dict['head']
    if a_f.is_valid() and h_f.is_valid():
      A = a_f.save()
      U = h_f.save()
      #organisation
      if ty == Member.ORG:
        o = a_f.cleaned_data['organisation']
        O = Organisation(name=o,address=A)

        # add head-of-list permissions
        is_hol_d = Permission.objects.get(codename='MEMBER')
        U.user_permissions.add(is_hol_d)

        # delegate
        delegate = h_f.cleaned_data['delegate']
        if delegate:
          d_f = form_dict['delegate']
          if d_f.is_valid():
            D = d_f.save()

      #student
      if ty == Member.STD:
        sp_f = form_dict['student_proof']
        if sp_f.is_valid():
          M = sp_f.save(commit=False)
          M.id=m_id
          M.type=ty

      if M == None: M = Member(id=m_id,type=ty)

      # add member_id and head_of_list to Member model
      if ty == Member.ORG: M.organisation = O
      M.address=A
      M.head_of_list=U
      M.save()
      if D != None: M.users.add(D)

      g_f = form_dict['group']
      if g_f.is_valid():
        Gs = g_f.cleaned_data['groups']
        add_to_groups(U,Gs)

      # build confirmation mail
      org_msg = ''
      if ty == Member.ORG:
        org_msg += '''
You are the head-of-list for ''' + unicode(O) + ''' giving you the privilege to manage the Member account 
and add further users (up to 6 in total).
'''
      message_content = {
        'FULLNAME': gen_fullname(M),
        'MEMBER_ID': m_id,
        'MEMBER_TYPE': Member.MEMBER_TYPES[ty][1],
	'ORGANISATION':	org_msg,
	'LOGIN': U.username,
#	'DEFAULT_WG': Group.objects.get(acronym='main'),
 	'WG': Gs,
      }

      # send confirmation
      subject = settings.TEMPLATE_CONTENT['reg']['register']['done']['title']
      ok=notify_by_email(subject,U.email,e_template,message_content)
      if not ok:
        return render(self.request,template, { 
				'mode': 'Error in email confirmation', 
				'message': settings.TEMPLATE_CONTENT['error']['email'],
		     })

      # generate invoice (this will send the invoice email implicitly)
#      generate_invoice(M)

      # redirect to thank you page
      return render(self.request,template, { 
				'mode': 'your Registration', 
				'message': render_to_string(settings.TEMPLATE_CONTENT['reg']['register']['done']['email_template'],message_content),
		   })

