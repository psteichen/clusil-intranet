# encoding=utf-8

from datetime import date

from django.conf import settings
from django.core.files import File

from members.functions import gen_fullname

from .models import Fee
from .invoice import draw_pdf

# gen invoice id
def invoice_id(m):
  i = 'INV_' + m.id + '_'+date.today().strftime('%Y')
  return i

# generate invoice
def generate_invoice(m,year=date.today().strftime('%Y')):
  from members.models import Member

  if m.type == Member.ORG:
    amount = settings.FEE[m.lvl]
  else:
    amount = settings.FEE[m.type]

  invoice_details = {
    'ID': invoice_id(m),
    'FULLNAME': gen_fullname(m.head_of_list),
    'DATE': date.today().strftime('%Y-%m-%d'),
    'YEAR': year,
    'AMOUNT': amount,
    'CURRENCY': settings.INVOICE['currency'],
  } 

  # generate pdf invoice
  from StringIO import StringIO
  pdf = StringIO()
  draw_pdf(pdf, m, invoice_details)
  pdf.seek(0)

  fn=invoice_details['ID'] + '.pdf'
 
  #save invoice in Fee model
  try:
    F = Fee.objects.get(member=m,year=year)
    F.invoice.save(fn,File(pdf),save=True)
  except Fee.DoesNotExist:
    F = Fee(member=m,year=year)
    F.invoice.save(fn,File(pdf),save=True)
  pdf.close()

  # send email
  from cms.functions import notify_by_email
  subject = settings.INVOICE['subject'] % m.id
  notify_by_email('board',m.head_of_list.email,subject,invoice_details,settings.INVOICE['mail_template'],File(pdf))

