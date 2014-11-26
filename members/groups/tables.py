#coding=utf-8

from django_tables2.tables import Table
from django_tables2 import Column

#from smash.tables import format_number, format_datetime

from .models import Group, Affiliation

#table for visualisation via django_tables2
class GroupTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  involvement	= Column(empty_values=())

  def render_row_class(self, value, record):
    if record.status == Group.STB:
      return 'info'

    if record.status == Member.ACT:
      return 'success'

  def render_involvement(self, value):
    try:
      count = Affiliation.objects.values(group=value).count()
      return unicode(count)
    except:
      return unicode('None')

  class Meta:
    model = Group
    fields = ( 'type', 'acronym', 'title', 'desc', 'involvement', )
    attrs = {"class": "table"}

