#coding=utf-8

from django_tables2.tables import Table
from django_tables2 import Column

from accounting.models import Fee

#table for visualisation via django_tables2
class InvoiceTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows

  def render_row_class(self, value, record):
    if record.paid:
      return 'success'

  class Meta:
    model = Fee
    fields = ( 'year', 'invoice', 'paid_date', )
    attrs = {"class": "table table-stripped"}


