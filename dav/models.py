from django.db.models import Model, CharField, FileField, ForeignKey

from django.contrib.auth.models import User

def sanitize_path(p):
  s_p = p.strip('<>%,:()[]{}@"&*#?^~\'')
  s_p = s_p.replace(' ','_').replace(',','_').replace('=','_')
  return s_p

class DavUpload(Model):
  def get_upload_path(self,fname):
    return self.path.lstrip('/') + sanitize_path(fname)

  user 	= ForeignKey(User)
  path 	= CharField(max_length=250)
  file 	= FileField(upload_to=get_upload_path)

  def __unicode__(self):
    return self.path + "/" + self.file.name

