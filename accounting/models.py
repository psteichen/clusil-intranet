from django.db.models import Model, ForeignKey, BooleanField, CharField, DateField, FileField

from members.models import Member

from .invoice import draw_pdf

def rename_invoice(i,f):
#  fn = rmf(i.member,'invoice',f)
#  return fn['name']+'.'+fn['ext']
  return 'INVOICE/'+f

# the "fee" model
class Fee(Model):
  member 	= ForeignKey(Member)
  paid 		= BooleanField(default=False)
  year 		= CharField(max_length=4)
  paid_date 	= DateField(blank=True,null=True)
  invoice 	= FileField(upload_to=rename_invoice)

  def __unicode__(self):  
    p = self.paid and ' - payed (' + self.paid_date + ')' or ''
    o = ''
    if self.member.type == Member.ORG: # organisation
      o += self.member.organisation.name + ' - head-of-list: '

    return self.member.id + ' (' + o + self.member.head_of_list.first_name + ' ' + unicode.upper(self.member.head_of_list.last_name) + ') - ' + self.year + p

  class Meta:
    unique_together = ('member', 'paid', 'year',)

