import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .forms import DavUploadForm

@login_required
def upload(r, path):

  if r.POST:
    upl_f = DavUploadForm(r.POST, r.FILES, FileSystemStorage())
    if upl_f.is_valid():
      f=upl_f.cleaned_data['file']
      p=upl_f.cleaned_data['path']
      upl=upl_f.save()
   
      message = """
      File: """ + f.name + """
      into folder: """ + p + """
      """
      return render(r, settings.TEMPLATE_CONTENT['dav']['upload']['done']['template'], {
			'title': settings.TEMPLATE_CONTENT['dav']['upload']['done']['title'],
			'message': settings.TEMPLATE_CONTENT['dav']['upload']['done']['message'] % {'file': f.name, 'folder': p,},
		})
    else:
      return render(r, settings.TEMPLATE_CONTENT['dav']['upload']['template'], {
			'title': settings.TEMPLATE_CONTENT['dav']['upload']['title'],
			'message': settings.TEMPLATE_CONTENT['dav']['upload']['desc'],
			'form': upl_f,
			'error': '[ERROR] in file uplod.',
		})
  else:
    if r.GET:
      parts=re.split('/',path)
      init_data= {
        'path': path,
      }
      return render(r, settings.TEMPLATE_CONTENT['dav']['upload']['template'], {
			'title': settings.TEMPLATE_CONTENT['dav']['upload']['title'],
			'message': settings.TEMPLATE_CONTENT['dav']['upload']['desc'],
			'form': DavUploadForm(initial=init_data),
			'submit': settings.TEMPLATE_CONTENT['dav']['upload']['submit'],
		})

    return render(r, settings.TEMPLATE_CONTENT['dav']['upload']['template'], {
			'title': settings.TEMPLATE_CONTENT['dav']['upload']['title'],
			'message': settings.TEMPLATE_CONTENT['dav']['upload']['desc'],
			'form': None,
			'error': '[ERROR] no path specified.',
		})

