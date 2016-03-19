# -*- coding: utf-8 -*-
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from django.conf import settings

from members.functions import get_country_from_address
from members.models import Member

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
        u'CLUSIL a.s.b.l. co/ SMILE g.i.e.',
        u'41, ave de la gare L-1611 Luxembourg',
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
  textobject.textLine(member.head_of_list.first_name + ' ' + unicode.upper(member.head_of_list.last_name))
  if member.type == Member.ORG:
    textobject.textLine(member.organisation.name)
  textobject.textLine(member.address.street)
  textobject.textLine(member.address.postal_code + ' ' + member.address.town)
  textobject.textLine(get_country_from_address(member.address))
  canvas.drawText(textobject)

  # summary
  textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
  textobject.textLine(u'Invoice ID: %s' % details['ID'])
  textobject.textLine(u'Invoice Date: %s' % details['DATE'])
  if member.type == Member.ORG:
    textobject.textLine(u'Member head-of-list: %s' % details['FULLNAME'])
  else:
    textobject.textLine(u'Member: %s' % details['FULLNAME'])
  textobject.textLine(u'Membership type: %s' % Member.MEMBER_TYPES[member.type][1])
  canvas.drawText(textobject)

  # details
  data = [[u'Member', u'Fee'], ]
  #head-of-list:
  data.append([
      member.head_of_list.first_name + ' ' + unicode.upper(member.head_of_list.last_name),
      '',
    ])

  if member.type == Member.ORG:
    #delegate:
    if member.delegate:
      data.append([
          member.delegate.first_name + ' ' + unicode.upper(member.delegate.last_name),
          '',
        ])

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
