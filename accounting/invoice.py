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
    canvas.setStrokeColorRGB(0,0.5,1)
    canvas.setFont('Helvetica', 16)
    canvas.drawString(10 * cm, -1.5 * cm, 'INVOICE')
    canvas.drawInlineImage(settings.ACCOUNTING['invoice']['logo'], 17.5 * cm, -2.1 * cm, 100, 50)
    canvas.setLineWidth(4)
    canvas.line(0, -2.5 * cm, 21.7 * cm, -2.5 * cm)


def draw_address(canvas):
    """ Draws the business address """
    canvas.setFont('Helvetica', 9)
    business_details = (
        u'CLUSIL a.s.b.l.',
        u'41, ave de la gare L-1611 Luxembourg',
        u'info@clusil.lu - www.clusil.lu',
        u'RCS Luxembourg: F3043',
    )
    textobject = canvas.beginText(1 * cm, -1 * cm)
    for line in business_details:
        textobject.textLine(line)
    canvas.drawText(textobject)


def draw_footer(canvas):
    """ Draws the invoice footer """
    canvas.setFont('Helvetica', 9)
    canvas.setStrokeColorRGB(0,0.5,1)
    canvas.setLineWidth(4)
    canvas.line(0, -27.5 * cm, 21.7 * cm, -27.5 * cm)
    footer = (
        u'IBAN: LU23 0030 7724 6992 0000',
        u'BIC: BGLLULL',
    )
    textobject = canvas.beginText(15 * cm, -28.5 * cm)
    for line in footer:
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

  # title
  canvas.setFont('Helvetica', 14)
  textobject = canvas.beginText(5.5 * cm, -6.75 * cm)
  textobject.textLine(u'Invoice for the CLUSIL membership for %s' % details['YEAR'])
  canvas.drawText(textobject)

  canvas.setFont('Helvetica', 10)

  # invoice summary
  textobject = canvas.beginText(1.5 * cm, -8 * cm)
  textobject.textLine(u'Invoice ID: %s' % details['ID'])
  textobject.textLine(u'Invoice Date: %s' % details['DATE'])
  canvas.drawText(textobject)

  # membership summary
  textobject = canvas.beginText(1.5 * cm, -9.5 * cm)
  textobject.textLine(u'Membership type: %s' % Member.MEMBER_TYPES[member.type][1])
  if member.type == Member.ORG:
    textobject.textLine(u'Head-of-list: %s' % details['FULLNAME'])
  else:
    textobject.textLine(u'Member: %s' % details['FULLNAME'])
  if member.type == Member.ORG:
    textobject.textLine(u'Nb of registered people: %i' % member.lvl)
  canvas.drawText(textobject)

  # list of people
  textobject = canvas.beginText(2.5 * cm, -11 * cm)
  #head-of-list:
  textobject.textLine(' - ' + member.head_of_list.first_name + ' ' + unicode.upper(member.head_of_list.last_name))
  if member.type == Member.ORG:
    #delegate:
    if member.delegate:
      textobject.textLine(' - ' + member.delegate.first_name + ' ' + unicode.upper(member.delegate.last_name))

    for u in member.users.all():
      textobject.textLine(' - ' + u.first_name + ' ' + unicode.upper(u.last_name))
  canvas.drawText(textobject)

  offset = member.users.count() / 3
  # fee 
  textobject = canvas.beginText(2.5 * cm, -(14+offset) * cm)
  textobject.textLine(u'Total amount of the CLUSIL membership fee: %s' % unicode(details['AMOUNT']) + u' EUR')
  canvas.drawText(textobject)

  # thank you message 
  textobject = canvas.beginText(1.5 * cm, -(16+offset) * cm)
  textobject.textLine(u'Thank you for being a CLUSIL member.')
  textobject.textLine(u'Please be so kind and pay the membership fee within the next two weeks.')
  canvas.drawText(textobject)

  canvas.showPage()
  canvas.save()
