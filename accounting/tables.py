#coding=utf-8

from django.config import settings
from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from .models import Fee

#table for visualisation via django_tables2
class InvoiceTable(Table,actions=False):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  payment      	= Column(verbose_name='Validate payment',empty_values=())
  invoice 	= Column(verbose_name='Credit Note',empty_values=())
  credit 	= Column(verbose_name='New Invoice',empty_values=())

  def render_row_class(self, value, record):
    if record.paid:
      return 'success'

  def render_payment(self, record):
    link = '<center><a class="btn btn-'+self.actions['payment']['grade']+' btn-sm" href="'+self.actions['payment']['url']+'{}"><span class="glyphicon glyphicon-'+self.actions['payment']['icon']+'"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  def render_invoice(self, record):
    link = '<center><a class="btn btn-'+self.actions['invoice']['grade']+' btn-sm" href="'+self.actions['invoice']['url']+'{}"><span class="glyphicon glyphicon-'+self.actions['invoice']['icon']+'"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  def render_credit(self, record):
    link = '<center><a class="btn btn-'+self.actions['credit']['grade']+' btn-sm" href="'+self.actions['credit']['url']+'{}"><span class="glyphicon glyphicon-'+self.actions['credit']['icon']+'"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  class Meta:
    model = Fee
    fields = ( 'year', 'member.organisation', 'invoice', 'paid', 'paid_date', 'payment', 'invoice', 'crtedit' )
    attrs = {"class": "table table-stripped"}


