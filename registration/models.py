from django.db.models import Model, DateTimeField, IntegerField, CharField, ForeignKey

from members.models import Member

# Registration model
class Registration(Model):
  OK	= 0
  NOK	= 1
  VALIDATED = (
    (OK	,'OK'),
    (NOK,'NOK'),
  )

  member 		= ForeignKey(Member)
  hash_code 		= CharField(max_length=50)
  date_of_registration 	= DateTimeField()
  validated 		= IntegerField(choices=VALIDATED,default=NOK)
  date_of_validation 	= DateTimeField(blank=True,null=True)
 
  def __unicode__(self):
    return unicode(self.member) + ' [ ' + self.hash_code + ' ] - ' + self.VALIDATED[self.validated][1]

