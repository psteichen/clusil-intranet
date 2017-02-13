
from django.forms import Form, ModelChoiceField, CharField, FileField, Textarea

class IdeaForm(Form):
  content	= CharField(label='Detail your thought',max_length=2500,widget=Textarea(attrs={'cols': 20, 'rows': 5, }))
  file 		= FileField(label='Attach file')

