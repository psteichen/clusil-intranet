# encoding=utf-8

from datetime import date

from django.conf import settings
from django.core.files import File

from members.functions import gen_fullname

from .models import Fee
from .invoice import draw_pdf as pdf_invoice
from .credit import draw_pdf as pdf_credit

# gen invoice id
def invoice_id(m):
  i = 'INV_' + m.id + '_'+date.today().strftime('%Y')
  return i

# generate invoice
def generate_invoice(m,year=date.today().strftime('%Y')):
  from members.models import Member

  INV = settings.ACCOUNTING['invoice']

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
    'CURRENCY': INV['currency'],
  } 

  # generate pdf invoice
  from StringIO import StringIO
  pdf = StringIO()
  pdf_invoice(pdf, m, invoice_details)
  pdf.seek(0)

  fn=invoice_details['ID'] + '.pdf'
 
  # create attachement
  from email.mime.application import MIMEApplication
  attachment = MIMEApplication(pdf.read())
  attachment.add_header("Content-Disposition", "attachment",filename=fn)

  #save invoice in Fee model
  try:
    F = Fee.objects.get(member=m,year=year)
    F.paid_date = None
    F.invoice.save(fn,File(pdf),save=True)
  except Fee.DoesNotExist:
    F = Fee(member=m,year=year)
    F.paid_date = None
    F.invoice.save(fn,File(pdf),save=True)
  pdf.close()

  # send email
  from cms.functions import notify_by_email
  subject = INV['subject'] % m.id
  notify_by_email(m.head_of_list.email,subject,invoice_details,INV['mail_template'],attachment)


# gen credit note id
def credit_id(m):
  i = 'CRED_' + m.id + '_'+date.today().strftime('%Y')
  return i

# generate credit note
def generate_credit_note(m):
  from members.models import Member

  CRED = settings.ACCOUNTING['credit']

  if m.type == Member.ORG:
    amount = settings.FEE[m.lvl]
  else:
    amount = settings.FEE[m.type]

  credit_details = {
    'ID': credit_id(m),
    'FULLNAME': gen_fullname(m.head_of_list),
    'DATE': date.today().strftime('%Y-%m-%d'),
    'AMOUNT': amount,
    'CURRENCY': CRED['currency'],
  } 

  # generate pdf credit note
  from StringIO import StringIO
  pdf = StringIO()
  pdf_credit(pdf, m, credit_details)
  pdf.seek(0)

  fn=credit_details['ID'] + '.pdf'
 
  # create attachement
  from email.mime.application import MIMEApplication
  attachment = MIMEApplication(pdf.read())
  attachment.add_header("Content-Disposition", "attachment",filename=fn)

  pdf.close()

  # send email
  from cms.functions import notify_by_email
  subject = CRED['subject'] % m.id
  notify_by_email(m.head_of_list.email,subject,credit_details,CRED['mail_template'],attachment)

