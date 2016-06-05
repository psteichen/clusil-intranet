
from django.forms import Form, CharField, FileField

class UploadForm(Form):
  file 		= FileField(label='Upload file')

