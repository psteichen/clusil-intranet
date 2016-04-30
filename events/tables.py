# coding=utf-8

from datetime import date

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from members.functions import gen_fullname
from attendance.models import Event_Attendance

from .models import Event

#table for visualisation via django_tables2
class EventTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  details	= Column(verbose_name='Details',empty_values=())
  send		= Column(verbose_name='Send invitations',empty_values=())
  modify	= Column(verbose_name='Modify',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_details(self, record):
    link = '<a class="btn btn-info btn-sm" href="/events/list/{}/"><span class="glyphicon glyphicon-list"></span></a>'.format(escape(record.pk))
    return mark_safe(link)
 
  def render_send(self, record):
    sent = None
    try:
      I = Invitation.objects.get(meeting=record)
      sent = I.sent
    except: pass
    if sent: #already sent, resend?
      link = '<center><a class="btn btn-success btn-sm" href="/events/send/{}/" title="Renvoyer"><span class="glyphicon glyphicon-envelope"></span></a></center>'.format(escape(record.id))
    else: #not yet sent
      link = '<center><a class="btn btn-danger btn-sm" href="/events/send/{}/" title="Envoyer"><span class="glyphicon glyphicon-envelope"></span></a></center>'.format(escape(record.id))

    return mark_safe(link)

  def render_modify(self, record):
    link = '<center><a class="btn btn-danger btn-sm" href="/events/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  class Meta:
    model = Event
    fields = ( 'title', 'when', 'location', 'details', )
    attrs = {"class": "table table-striped"}
