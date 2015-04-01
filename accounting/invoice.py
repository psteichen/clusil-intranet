# -*- coding: utf-8 -*-
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from django.conf import settings

def draw_header(canvas):
    """ Draws the invoice header """
    canvas.setStrokeColorRGB(0.02,0.5,0.3)
#    canvas.setFillColorRGB(0.02,0.5,0.3)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(18 * cm, -1.2 * cm, 'INVOICE')
    canvas.drawInlineImage(settings.INVOICE['logo'], 8.5 * cm, -1.8 * cm, 250, 50)
    canvas.setLineWidth(4)
    canvas.line(0, -2 * cm, 21.7 * cm, -2 * cm)


def draw_address(canvas):
    """ Draws the business address """
    business_details = (
        u'CLUSIL a.s.b.l. co/ CRP Henri Tudor',
        u'29 av. JF Kennedy L-1855 Luxembourg-Kirchberg',
        u'info@clusil.lu - www.clusil.lu',
        u'RCS Luxembourg: F3043'
    )
    canvas.setFont('Helvetica', 9)
    textobject = canvas.beginText(1 * cm, -0.5 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def draw_footer(canvas):
    """ Draws the invoice footer """
    note = (
        u'IBAN: LUxx xxxx xxxx xxxx xxxx - BIC: BGLLULL',
    )
    textobject = canvas.beginText(1 * cm, -27 * cm)
    for line in note:
        textobject.textLine(line)
    canvas.drawText(textobject)

def draw_pdf(buffer, member, details):
  from members.models import Member
  """ Draws the invoice """
  canvas = Canvas(buffer, pagesize=A4)
  canvas.translate(0, 29.7 * cm)
  canvas.setFont('Helvetica', 10)

  canvas.saveState()
  draw_header(canvas)
  canvas.restoreState()

  canvas.saveState()
  draw_footer(canvas)
  canvas.restoreState()

  canvas.saveState()
  draw_address(canvas)
  canvas.restoreState()

  # member address (aka head-of-list contact details)
  textobject = canvas.beginText(13 * cm, -3.5 * cm)
  textobject.textLine(member.firstname + ' ' + unicode.upper(member.lastname))
  if member.member_type == 1:
    textobject.textLine(member.organisation)
  textobject.textLine(member.address)
  textobject.textLine(member.postal_code + ' ' + member.town)
  textobject.textLine(member.country)
  canvas.drawText(textobject)

  # summary
  textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
  textobject.textLine(u'Invoice ID: %s' % details['ID'])
  textobject.textLine(u'Invoice Date: %s' % details['DATE'])
  if member.member_type == 1:
    textobject.textLine(u'Member head-of-list: %s' % details['FULLNAME'])
  else:
    textobject.textLine(u'Member: %s' % details['FULLNAME'])
  textobject.textLine(u'Membership type: %s' % Member.MEMBER_TYPES[member.member_type][1])
  canvas.drawText(textobject)

  # details
  data = [[u'Member', u'Fee'], ]
  for u in member.users.all():
    data.append([
        u.first_name + ' ' + unicode.upper(u.last_name),
        '',
    ])
  data.append([u'Total:', details['AMOUNT']])
  table = Table(data, colWidths=[11 * cm, 3 * cm])
  table.setStyle([
      ('FONT', (0, 0), (-1, -1), 'Helvetica'),
      ('FONTSIZE', (0, 0), (-1, -1), 10),
      ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
      ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
      ('GRID', (-2, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
      ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
      ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
  ])
  tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
  table.drawOn(canvas, 1 * cm, -9 * cm - th)

  canvas.showPage()
  canvas.save()
