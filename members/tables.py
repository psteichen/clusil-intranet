#coding=utf-8

from datetime import date

from django_tables2.tables import Table
from django_tables2 import Column

#from smash.tables import format_number, format_datetime

from .models import Member, Role

#table for visualisation via django_tables2
class MemberTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows

  def render_row_class(self, value, record):
    if record.status == Member.STB:
      return 'warning'

    if record.status == Member.WBE:
      return 'info'

    if record.status == Member.ACT:
      return 'success'

    if record.end_date:
      return 'danger'

#  def render_start_date(self, value):
#    return format_datetime(value)

#  def render_end_date(self, value):
#    return format_datetime(value)

  class Meta:
    model = Member
    fields = ( 'id', 'type', 'head_of_list', 'delegate', 'status', )
    attrs = {"class": "table"}


