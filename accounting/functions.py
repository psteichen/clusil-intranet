from .invoice import draw_pdf

# gen invoice id
def invoice_id(m):
  i = rmf(m,'invoice')['name']

  return i + '_' + date.today().strftime('%Y')

# generate invoice
def generate_invoice(m):
  invoice_details = {
    'ID': invoice_id(m),
    'FULLNAME': gen_fullname(m),
    'DATE': date.today().strftime('%Y-%m-%d'),
    'AMOUNT': settings.FEE[m.member_type],
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


