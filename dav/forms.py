from django.forms import ModelForm, HiddenInput

from .models import DavUpload

class DavUploadForm(ModelForm):

  class Meta:
    model = DavUpload
    widgets = {
      'user'	: HiddenInput(),
      'path'	: HiddenInput(),
    }
