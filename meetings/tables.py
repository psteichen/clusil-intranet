# coding=utf-8

from datetime import date

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from members.functions import gen_fullname

from .models import Meeting

#table for visualisation via django_tables2
class MeetingTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Présents/Excusés',empty_values=())
  details	= Column(verbose_name='Détails',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_attendance(self, value):
    return 'blabla'

#    return ' ; '.join([gen_fullname(a) for a in value.all()])

#  def render_excused(self, value):
#    return ' ; '.join([gen_fullname(e) for e in value.all()])

  def render_totals(self, record):
    return '{} / {}'.format(record.attendance.all().count(),record.excused.all().count())

  def render_details(self, record):
    link = '<a class="btn btn-default btn-sm" href="/meetings/list/{}/"><span class="glyphicon glyphicon-list"></span></a>'.format(escape(record.num))
    return mark_safe(link)

  class Meta:
    model = Meeting
#    fields = ( 'title', 'when', 'location', 'attendance.all()', 'excused.all()', 'totals',)
    fields = ( 'title', 'when', 'location', 'attendance', 'totals', 'details', )
    attrs = {"class": "table table-striped"}
