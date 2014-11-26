from django.db.models import Model, ForeignKey, BooleanField, CharField, DateField, FileField

from intranet.functions import rmf
from members.models import Member

from .invoice import draw_pdf

def rename_invoice(i,f):
  fn = rmf(i,'invoice',f)
  return fn['name']+'.'+fn['ext']

# the "fee" model
class Fee(Model):
  member 	= ForeignKey(Member)
  paid 		= BooleanField()
  year 		= CharField(max_length=4)
  paid_date 	= DateField()
  invoice 	= FileField(upload_to=rename_invoice)

  def __unicode__(self):  
    p = self.paid and ' - payed (' + self.paid_date + ')' or ''
    o = ''
    if self.member.member_type == 1: # organisation
      o += self.member.organisation + ' - head-of-list: '

    return self.member.member_id + ' (' + o + self.member.firstname + ' ' + unicode.upper(self.member.lastname) + ') - ' + self.year + p

  class Meta:
    unique_together = ('member', 'paid', 'year',)

