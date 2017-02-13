
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.template.loader import render_to_string

from cms.functions import notify_by_email
from members.functions import gen_fullname

from .forms import IdeaForm

# generic ideabox view #
########################
def gen_ideabox_message(user,idea):
  content = { 
	'name'	: gen_fullname(user),
	'idea'	: unicode(idea),
  }

  return render_to_string(settings.TEMPLATE_CONTENT['ideabox']['email']['template'],content)

def submit_idea(r):

  template 	= settings.TEMPLATE_CONTENT['ideabox']['template']
  title 	= settings.TEMPLATE_CONTENT['ideabox']['title']
  desc		= settings.TEMPLATE_CONTENT['ideabox']['desc'].format(first_name=r.user.first_name,last_name=r.user.last_name,username=r.user.username)
  submit	= settings.TEMPLATE_CONTENT['ideabox']['submit']

  subject 	= settings.TEMPLATE_CONTENT['ideabox']['email']['subject']
  to 		= settings.TEMPLATE_CONTENT['ideabox']['email']['to']

  done_template = settings.TEMPLATE_CONTENT['ideabox']['done']['template']
  done_title 	= settings.TEMPLATE_CONTENT['ideabox']['done']['title']

  if r.POST:
    idf = IdeaForm(r.POST, r.FILES)
    if idf.is_valid():
      idea 	= idf.cleaned_data['content']
      attach 	= idf.cleaned_data['file']

      # build mail
      message = gen_ideabox_message(r.user,idea)
      message_content = {
          'FULLNAME'    : 'BOARD',
          'MESSAGE'     : message,
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

