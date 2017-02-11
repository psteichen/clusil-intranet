
from django.forms import Form, CharField, FileField
from django.contrib.auth.models import User

class IdeaForm(Form):
  user		= ForeignKey(User)
  content	= CharField(label='Detail your thought',max_length=2500)
  file 		= FileField(label='Attach file')

