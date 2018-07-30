#coding=utf-8

from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from cms.functions import visualiseDateTime
from cms.tables import gen_table_actions

from .models import Fee

#table for visualisation via django_tables2
class InvoiceTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  actions      	= Column(verbose_name='Actions',empty_values=())

  def render_row_class(self, value, record):
    if record.paid:
      return 'success'

  def render_paid(self, value, record):
    if value and record.paid_date: #paid
      return mark_safe('<span class="glyphicon glyphicon-ok"></span>&nbsp;&nbsp;('+visualiseDateTime(record.paid_date)+')')
    else:
      return mark_safe('<span class="glyphicon glyphicon-remove"></span>')

  def render_actions(self, value, record):
    actions = settings.TEMPLATE_CONTENT['accounting']['actions']['table']
    return gen_table_actions(actions,{'id':record.member.id,'year':record.year})

  class Meta:
    model = Fee
    fields = ( 'year', 'member.gen_name', 'invoice', 'paid', 'actions', )
    attrs = {"class": "table table-stripped"}


