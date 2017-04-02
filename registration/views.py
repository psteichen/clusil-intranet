# -*- coding: utf-8 -*-
from datetime import date

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render 
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import make_password

from cms.functions import show_form, notify_by_email, replicate_to_ldap, debug

from members.functions import get_members_to_validate, gen_member_fullname, activate_member
from members.models import Member, Organisation, Address, Role
from members.groups.models import Group, Affiliation

from .models import Registration
from .functions import gen_member_id, add_to_groups, gen_username, gen_random_password, gen_hash, gen_confirmation_link, gen_user_list


##
## registration helper functions
##
def show_delegate_form(wizard):
  if wizard.kwargs: #alt mode 
    [item for item in Member.MEMBER_TYPES if item[0] == wizard.kwargs['type']]
    ty = int(item[0])
    return ty == Member.ORG and show_form(wizard,'head','delegate',True)
  else: #normal mode
    return show_form(wizard,'type','member_type',Member.ORG) and show_form(wizard,'head','delegate',True)

def show_multi_user_form(wizard):
  if wizard.kwargs: #alt mode 
    [item for item in Member.MEMBER_TYPES if item[0] == wizard.kwargs['type']]
    ty = int(item[0])
    return ty == Member.ORG
  else: #normal mode
    return show_form(wizard,'type','member_type',Member.ORG)

def show_student_proof_form(wizard):
  if wizard.kwargs: #alt mode 
    [item for item in Member.MEMBER_TYPES if item[0] == wizard.kwargs['type']]
    ty = int(item[0])
    return ty == Member.STD
  else: #normal mode
    return show_form(wizard,'type','member_type',Member.STD)


###########################
# registration formwizard #
###########################
class RegistrationWizard(SessionWizardView):
  file_storage = FileSystemStorage()

  def get_template_names(self):
    return 'wizard.html'

  def get_context_data(self, form, **kwargs):
    context = super(RegistrationWizard, self).get_context_data(form=form, **kwargs)

    ty = None
    if self.kwargs: 
      ty = self.kwargs['type']
    else:
      cleaned_data = self.get_cleaned_data_for_step('type') or False
      if cleaned_data: ty = Member.MEMBER_TYPES[int(cleaned_data['member_type'])][1]

    self.request.breadcrumbs( ( 
				('registration ['+unicode(ty)+']','/reg/'+unicode(ty)+'/'),
                             ) )


    if self.steps.current != None:
      if self.request.user.has_perm('cms.SECR'):
        context.update({'title': settings.TEMPLATE_CONTENT['reg']['board_reg']['title'].format(type=ty)})
        context.update({'step_desc': ''})
      else:
        context.update({'title': settings.TEMPLATE_CONTENT['reg']['register']['title'].format(type=ty)})
        context.update({'step_desc': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['desc']})

      context.update({'step_title': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['title']})
      context.update({'first': settings.TEMPLATE_CONTENT['reg']['register']['first']})
      context.update({'prev': settings.TEMPLATE_CONTENT['reg']['register']['prev']})
      context.update({'next': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['next']})

    if self.steps.current == 'head':
      if unicode(ty) != unicode(Member.MEMBER_TYPES[Member.ORG]):
        context.update({'step_title': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['alttitle']})
        context.update({'step_desc': settings.TEMPLATE_CONTENT['reg']['register'][self.steps.current]['altdesc']})

    return context

  def get_form(self, step=None, data=None, files=None, **kwargs):
    form = super(RegistrationWizard, self).get_form(step, data, files)

    # determine the step if not given
    if step is None:
      step = self.steps.current

    ty = None
    if self.kwargs: 
      [item for item in Member.MEMBER_TYPES if item[0] == self.kwargs['type']]
      ty = int(item[0])

    if step == 'address':
      cleaned_data = self.get_cleaned_data_for_step('type') or False
      if cleaned_data: # we're in normal mode 
        ty = int(cleaned_data['member_type'])
      if ty == Member.ORG:
        del form.fields['first_name']
        del form.fields['last_name']
        del form.fields['email']
      if ty != Member.ORG:
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
      t_data = self.get_cleaned_data_for_step('type') or False
      if t_data:
        ty = int(t_data['member_type'])
      if ty != Member.ORG:
        del form.fields['delegate']
        del form.fields['more']

    if step == 'delegate':
      del form.fields['delegate']
      del form.fields['more']

    if step == 'more':
      head_data = self.get_cleaned_data_for_step('head') or False
      if head_data:
        ex = int(head_data['more'])
        del_data = self.get_cleaned_data_for_step('delegate') or False
	if del_data: form.extra = ex-1
	else: form.extra = ex

    return form

  def done(self, fl, form_dict, **kwargs):
    self.request.breadcrumbs( ( 
				('registration','/reg/'),
                            ) )

    done_title = settings.TEMPLATE_CONTENT['reg']['register']['done']['title']
    done_template = settings.TEMPLATE_CONTENT['reg']['register']['done']['template']
    error_template = settings.TEMPLATE_CONTENT['reg']['register']['done']['error_template']
    email_template = settings.TEMPLATE_CONTENT['reg']['register']['done']['email_template']

    m_id = gen_member_id()

    M = lvl = O = A = U = D = Gs = None
    Us = []

    ty = None
    if self.kwargs: 
      [item for item in Member.MEMBER_TYPES if item[0] == self.kwargs['type']]
      ty = int(item[0])
    else: 
      t_f = form_dict['type']
      ty = int(t_f.cleaned_data['member_type'])

    a_f = form_dict['address']
    h_f = form_dict['head']
    if a_f.is_valid() and h_f.is_valid():
      A = a_f.save()
      U = h_f.save()
      #role for hol
      Ro = Role(title="Head of List",user=U)
      Ro.save()
      #organisation
      if ty == Member.ORG:
        o = a_f.cleaned_data['organisation']
        O = Organisation(name=o,address=A)
        O.save()
  
        #get nb of users
        lvl = int(h_f.cleaned_data['more'])+1 #add one for head-of-list

        # delegate
        delegate = h_f.cleaned_data['delegate']
        if delegate:
          d_f = form_dict['delegate']
          if d_f.is_valid():
            D = d_f.save()
            D.save()

            #role for delegate
            Ro = Role(title="Delegate",user=D)
            Ro.save()

        #all users for ORG type
        mu_fs = form_dict['more']
        if mu_fs.is_valid():
          for u in mu_fs:
            if u.is_valid() and u.has_changed(): 
              if u.cleaned_data['email']:
                user = u.save(commit=False)
                user.username = gen_username(user.first_name,user.last_name)
                user.is_active = False
                user.password = make_password(gen_random_password())
                user.save()
                Us.append(user)


      #student
      if ty == Member.STD:
        sp_f = form_dict['student_proof']
        if sp_f.is_valid():
          M = sp_f.save(commit=False)
          M.pk=m_id
          M.type=ty

      if M == None: M = Member(pk=m_id,type=ty)

      # if of type org, add organisation to Member model
      if ty == Member.ORG: M.organisation = O

      # add address and head_of_list to Member model
      M.address=A
      M.head_of_list=U

      #set the level (number of users) for ORG type
      if lvl: M.lvl=lvl

      # add delegate if exists
      if D != None: M.delegate=D

      # save Member model
      M.save()
      # add all Users for ORG type
      if Us != []: M.users=Us

#      g_f = form_dict['group']
#      if g_f.is_valid():
#        Gs = g_f.cleaned_data['groups']
#        add_to_groups(U,Gs)

      reg_hash_code = gen_hash(settings.REG_SALT,M.head_of_list.email,15,M.address)
      # create registration entry for out-of-bound validation
      R = Registration(member=M,hash_code=reg_hash_code,date_of_registration=timezone.now())
      R.save()

      # build confirmation mail
      message_content = {
        'FULLNAME'	: gen_member_fullname(M),
        'MEMBER_TYPE'	: Member.MEMBER_TYPES[int(M.type)][1],
	'LINK'		: gen_confirmation_link(reg_hash_code),
      }
      # send confirmation
      ok=notify_by_email(M.head_of_list.email,done_title,message_content,email_template)
      if not ok:
        return render(self.request, error_template, { 
				'mode': 'Error in email confirmation', 
				'message': settings.TEMPLATE_CONTENT['error']['email'],
		     })

      head = False
      if int(M.type) == int(Member.ORG): head = True
   
      # done, redirect to thank you page
      return render(self.request, done_template, { 
			'title'	: done_title,
        		'name'	: gen_member_fullname(M),
        		'type'	: Member.MEMBER_TYPES[int(M.type)][1],
		        'head' 	: head,
		   })



###########################
# registration validation #
###########################
def validate(r, val_hash):

  title 		= settings.TEMPLATE_CONTENT['reg']['validate']['title']
  template		= settings.TEMPLATE_CONTENT['reg']['validate']['template']
  done_message		= settings.TEMPLATE_CONTENT['reg']['validate']['done_message']
  error_message		= settings.TEMPLATE_CONTENT['reg']['validate']['error_message']
  email_template	= settings.TEMPLATE_CONTENT['reg']['validate']['email']['template']
  org_msg		= settings.TEMPLATE_CONTENT['reg']['validate']['email']['org_msg']
  users_msg		= settings.TEMPLATE_CONTENT['reg']['validate']['email']['users_msg']

  M = R = None

  debug('reg','hash == ' + val_hash)

  try:
    # if hash code match: it's a member to be validated
    R = Registration.objects.get(hash_code=str(val_hash))
    debug('reg','valid hash found')
    if R.validated != R.OK: M = R.member
  except Registration.DoesNotExist:
    # check if validation by Board member
    if r.user.is_authenticated():
      debug('reg','user is logged in (!)')
      if r.user.has_perm('cms.BOARD'):
        debug('reg','user is board member!')
        #admin validation: val_hash == member_id
        R = Registration.objects.get(member=Member.objects.get(id=str(val_hash)))
        if R.validated != R.OK: M = R.member

  debug('reg','Member is :' + unicode(M))

  if M != None:
    # activate member
    activate_member(M)

    # save registration as OK
    R.date_of_validation = timezone.now()
    R.validated = R.OK
    R.save()

    message = done_message.format(name=gen_member_fullname(M),member_id=M.pk)

    #notify by email
    message_content = {
        'FULLNAME'	: gen_member_fullname(M),
        'MEMBER_ID'	: M.pk,
        'MEMBER_TYPE'	: Member.MEMBER_TYPES[int(M.type)][1],
        'USERNAME'	: M.head_of_list.username,
        'CMS_URL'	: 'https://'+settings.ALLOWED_HOSTS[0]+'/',
    }
    if M.type == Member.ORG: 
      message_content['ORGANISATION']=org_msg.format(orga=M.organisation)
      message_content['USERS']=users_msg.format(users=gen_user_list(M))

    #send email
    ok=notify_by_email(M.head_of_list.email,title,message_content,email_template)

    return render(r, template, {
                   'title'	: title,
                   'message'	: message,
               })
  else: #error
    debug('reg','error, no valid hash found')
    return render(r, template, {
                   'title'		: title,
                   'error_message'	: error_message,
               })

  
