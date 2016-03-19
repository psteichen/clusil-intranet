from datetime import date

from django.conf import settings

from members.functions import gen_fullname

from .invoice import draw_pdf

# rename a file according to a member profile and mod (being a freely setable modifier)
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
  i = 'INV_' + m.id

  return i

# generate invoice
def generate_invoice(m):
  from members.models import Member

  if m.type == Member.ORG:
    amount = settings.FEE[m.lvl]
  else:
    amount = settings.FEE[m.type]

  invoice_details = {
    'ID': invoice_id(m),
    'FULLNAME': gen_fullname(m.head_of_list),
    'DATE': date.today().strftime('%Y-%m-%d'),
    'AMOUNT': amount,
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
  from cms.functions import notify_by_email
  subject = settings.INVOICE['subject'] % m.id
  notify_by_email('board',m.head_of_list.email,subject,invoice_details,settings.INVOICE['mail_template'],attachment)

