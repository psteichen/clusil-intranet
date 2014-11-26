# -*- coding: utf-8 -*-
from datetime import date

from django.conf import settings
from django.shortcuts import render 
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.formtools.wizard.views import SessionWizardView

from intranet.functions import show_form

from members.models import Member
from members.groups.models import Group, Affiliation


def show_delegate_form(wizard):
  return show_form(wizard,'type','member_type',Member.ORG)

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
        context.update({'step_desc': False})

    return context

  def get_form(self, step=None, data=None, files=None):
    form = super(RegistrationWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    if step == 'address':
      cleaned_data = self.get_cleaned_data_for_step('type') or {}
      if cleaned_data != {}:
        ty = cleaned_data['member_type']
        if ty != Member.ORG:
          del form.fields['organisation']
        if ty != Member.STD:
          del form.fields['student_proof']

    return form

  def done(self, fl, **kwargs):

    template = settings.TEMPLATE_CONTENT['reg']['register']['done']['template']
    e_template = settings.TEMPLATE_CONTENT['reg']['register']['done']['email_template']

    # reg and acces form
    if r_f.is_valid() and g_f.is_valid() and u_f.is_valid():

      m_id = gen_member_id()
      t = r_f.cleaned_data['member_type']
      n = r_f.cleaned_data['lastname']
      fn = r_f.cleaned_data['firstname']
      e = r_f.cleaned_data['email']
      o = r_f.cleaned_data['organisation']
      wg = wg_f.cleaned_data['wg']
      u = u_f.cleaned_data['username']

      # some basic checks according to member types

      # if type=std, student proof file must be present
      if int(t) == 2: # student
        # proof document must be uploaded
        try:
          sp = r.FILES['student_proof']
        except:
          return render(r,'reg.html', {'reg_form': r_f, 'wg_form': wg_f, 'user_form': u_f, 'captcha': display_captcha(), 'error_message': settings.TEMPLATE_CONTENT['error']['std']})

      # if type=org, org field must be filled out
      if int(t) == 1: # organisation
        if o == '':
          return render(r,'reg.html', {'reg_form': r_f, 'wg_form': wg_f, 'user_form': u_f, 'captcha': display_captcha(), 'error_message': settings.TEMPLATE_CONTENT['error']['org']})

            # add first and last name as well as email to the User model
      U = u_f.save(commit=False)
      U.first_name = fn
      U.last_name = n
      U.email = e
      U.save()
      # add head-of-list permissions
      is_hol_d = Permission.objects.get(codename='is_hol_d')
      U.user_permissions.add(is_hol_d)

      # add member_id and head_of_list to Member model
      M=r_f.save(commit=False)
      M.member_id=m_id
      M.head_of_list=U
      M.users=[U]
      M.save()

      # link member, user and WG (including the default WG)
      add_wg(U,wg)

      # build confirmation mail
      org_msg = ''
      if int(t) == 1: # organisation
        org_msg += '''
You are the head-of-list for ''' + o + ''' giving you the privilege to manage the Member account 
and add further users (up to 6 in total).
'''
      message_content = {
        'FULLNAME': gen_fullname(M),
        'MEMBER_ID': m_id,
        'MEMBER_TYPE': Member.MEMBER_TYPES[int(t)][1],
	'ORGANISATION':	org_msg,
	'LOGIN': u,
	'DEFAULT_WG': WG.objects.get(acronym='main'),
  	'WG': wg,
      }

      # send confirmation
      subject = settings.TEMPLATE_CONTENT['reg']['register']['done']['title'] % m_id
      ok=notify_by_email(subject,e,e_template,message_content)
      if not ok:
        return render(r,'reg.html', {'reg_form': r_f, 'wg_form': wg_f, 'user_form': u_f, 'captcha': display_captcha(), 'error_message': settings.TEMPLATE_CONTENT['error']['email']})

      # generate invoice (this will send the invoice email implicitly)
      generate_invoice(M)

      # redirect to thank you page
      return render(r,'done.html', {'mode': 'your Registration', 'message': render_to_string(settings.MAIL_CONFIRMATION['reg']['template'],message_content)})
    else:
      return render(r,'reg.html', {'reg_form': r_f, 'wg_form': wg_f, 'user_form': u_f, 'captcha': display_captcha(), 'error_message': settings.TEMPLATE_CONTENT['error']['gen']})

