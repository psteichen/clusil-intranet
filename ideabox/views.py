
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from cms.functions import notify_by_email
from members.functions import gen_fullname

from .forms import IdeaForm

# generic ideabox view #
########################
def submit_idea(r):

  template 	= settings.TEMPLATE_CONTENT['ideabox']['template']
  title 	= settings.TEMPLATE_CONTENT['ideabox']['title']
  desc		= settings.TEMPLATE_CONTENT['ideabox']['desc'],
  submit	= settings.TEMPLATE_CONTENT['ideabox']['submit'],

  subject 	= settings.TEMPLATE_CONTENT['ideabox']['email']['subject']
  to 		= settings.TEMPLATE_CONTENT['ideabox']['email']['to']
  message 	= settings.TEMPLATE_CONTENT['ideabox']['email']['message']

  done_template = settings.TEMPLATE_CONTENT['ideabox']['done']['template']
  done_title 	= settings.TEMPLATE_CONTENT['ideabox']['done']['title']

  if r.POST:
    idf = IdeaForm(r.POST, r.FILES)
    if idf.is_valid():
      user 	= idf.cleaned_data['user']
      idea 	= idf.cleaned_data['content']
      attach 	= r.FILES['file']

      # build mail
      message_content = {
          'FULLNAME'    : gen_fullname(user),
          'MESSAGE'     : idea,
      }
      # send idea to board
      ok=notify_by_email(to,subject,message_content,False,attach)
      if not ok:
        return render(r, error_template, { 
				'mode'		: 'Error in email confirmation', 
				'message'	: settings.TEMPLATE_CONTENT['error']['email'],
		     })

      #all fine -> show thank you message
      return render(r,done_template, {
			'title'		: done_title,
		   })

    else: #from not valid -> error
      return render(r,done_template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ' + gen_form_errors(idf),
		   })
  else:
    #no POST data yet -> show form
    form = IdeaForm()

    return render(r,template, {
			'title'	: title,
  			'desc'	: desc,
  			'submit': submit,
			'form'	: form,
		   })

