
from django.conf import settings
from django.shortcuts import render

from .forms import UploadForm
from .functions import handle_uploaded_file

# generic upload view #
#######################
def index(r,campaign='gen'):

  template = settings.TEMPLATE_CONTENT['upload']['template']
  title = settings.TEMPLATE_CONTENT['upload'][campaign]['title']

  e_template = settings.TEMPLATE_CONTENT['upload'][campaign]['email']['template']
  subject = settings.TEMPLATE_CONTENT['upload'][campaign]['email']['subject']
  to = settings.TEMPLATE_CONTENT['upload'][campaign]['email']['to']
  message = settings.TEMPLATE_CONTENT['upload'][campaign]['email']['message']

  done_template = settings.TEMPLATE_CONTENT['upload']['done']['template']
  done_title = settings.TEMPLATE_CONTENT['upload'][campaign]['done']['title']

  if r.POST:
    uf = UploadForm(r.POST, r.FILES)
    if uf.is_valid():
      f = r.FILES['file']

      # handle uploaded file
      handle_uploaded_file(f,campaign,subject,to,message,e_template)

      #all fine -> show thank you message
      message = settings.TEMPLATE_CONTENT['upload'][campaign]['done']['message']
      return render(r,done_template, {
			'title'		: done_title,
			'message'	: message,
		   })

    else: #from not valid -> error
      return render(r,done_template, {
			'title'		: title,
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ' + gen_form_errors(uf),
		   })
  else:
    #no POST data yet -> show form
    form = UploadForm()

    return render(r,template, {
			'title'	: title,
  			'desc'	: settings.TEMPLATE_CONTENT['upload'][campaign]['desc'],
  			'submit': settings.TEMPLATE_CONTENT['upload']['submit'],
			'form'	: form,
		   })


