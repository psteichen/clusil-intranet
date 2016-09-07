
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from .forms import UploadForm
from .functions import handle_uploaded_file, import_data

# generic upload view #
#######################
def upload(r,campaign='gen'):

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


# import_data #
###############
@permission_required('cms.BOARD')
def import_data(r,ty):

  template      = settings.TEMPLATE_CONTENT['upload']['import'][ty]['template']
  title         = settings.TEMPLATE_CONTENT['upload']['import'][ty]['title']
  desc          = settings.TEMPLATE_CONTENT['upload']['import'][ty]['desc']
  submit        = settings.TEMPLATE_CONTENT['upload']['import'][ty]['submit']

  done_template  = settings.TEMPLATE_CONTENT['upload']['import'][ty]['done']['template']
  done_title     = settings.TEMPLATE_CONTENT['upload']['import'][ty]['done']['title']
  done_message   = settings.TEMPLATE_CONTENT['upload']['import'][ty]['done']['message']

  if r.POST:
    uf = UploadForm(r.POST, r.FILES)
    if uf.is_valid():
      data      = uf.cleaned_data['file']

      # handle uploaded file
      errors = import_data(ty,data)

      if errors:
        # issue with import -> error
        return render(r, done_template, {
                               'title'          : done_title,
                               'error_message'  : settings.TEMPLATE_CONTENT['error']['gen'] + str(errors),
                    })

      # all fine -> done
      return render(r, done_template, {
                               'title'    : done_title,
                               'message'  : done_message,
                  })

    else:
      # form not valid -> error
      return render(r, done_template, {
                               'title'          : done_title,
                               'error_message'  : settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in idf.errors]),
                  })

  else:
    # no post yet -> empty form
    form = UploadForm()
    return render(r, template, {
                             'title'    : title,
                             'desc'     : desc,
                             'submit'   : submit,
                             'form'     : form,
                })
