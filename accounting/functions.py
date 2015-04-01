from datetime import date

from django.conf import settings

from members.functions import gen_fullname

from .models import Fee
from .invoice import draw_pdf

# rename the uploaded member files
def rmf(member, mod, filename=None):
  import os
  try:
    orig_name, orig_ext = os.path.splitext(filename)
  except:
    orig_ext = ''

  fn=member.id + os.sep + mod.upper() + '_' + member.head_of_list.first_name + ' ' + member.head_of_list.last_name.upper()
  if member.type == 1: # organisation
    fn += ' (' + unicode(member.organisation) + ')'

  import unicodedata
  return {'name': unicodedata.normalize('NFKD', fn).encode('ascii','ignore'),'ext': orig_ext}

# gen invoice id
def invoice_id(m):
  i = rmf(m,'invoice')['name']

  return i + '_' + date.today().strftime('%Y')

# generate invoice
def generate_invoice(m):
  invoice_details = {
    'ID': invoice_id(m),
    'FULLNAME': gen_fullname(m.head_of_list),
    'DATE': date.today().strftime('%Y-%m-%d'),
    'AMOUNT': Fee.MEMBER_FEES[m.type][1],
    'CURRENCY': settings.INVOICE['currency'],
  } 

  # generate pdf invoice
  from StringIO import StringIO
  pdf = StringIO()
  draw_pdf(pdf, m, invoice_details)
  pdf.seek(0)

  # create attachement
  from email.mime.application import MIMEApplication
  attachment = MIMEApplication(pdf.read())
  attachment.add_header("Content-Disposition", "attachment",filename=invoice_details['ID'] + '.pdf')
  pdf.close()

  # send email
  subject = settings.MAIL_CONFIRMATION['invoice']['subject'] % m.member_id
  confirm_by_email(subject,m.email,settings.MAIL_CONFIRMATION['invoice']['template'],invoice_details,attachment)


