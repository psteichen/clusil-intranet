#coding=utf-8

from datetime import date

from django_tables2.tables import Table
from django_tables2 import Column

from django.utils.safestring import mark_safe
from django.utils.html import escape

from .functions import get_all_users_for_membership
from .models import Member, Role

#table for visualisation via django_tables2
class MemberTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  member	= Column(verbose_name='Member',empty_values=())
  users		= Column(verbose_name='Users',empty_values=())
  details	= Column(verbose_name='Details',empty_values=())
  modify	= Column(verbose_name='Modify',empty_values=())

  def render_row_class(self, value, record):
    #TODO
    return ''

  def render_member(self, value, record):
    if record.type == Member.ORG:
      return unicode(record.organisation.name)
    else:
      name = unicode(record.head_of_list.first_name) + u' ' + unicode(record.head_of_list.last_name).upper()
      return name

  def render_head_of_list(self, value):
    name = unicode(value.first_name) + u' ' + unicode(value.last_name).upper()
    return name

  def render_users(self, value, record):
    users = get_all_users_for_membership(record)
    return len(users)

  def render_details(self, record):
    link = '<center><a class="btn btn-info btn-sm" href="/members/details/{}/"><span class="glyphicon glyphicon-list"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  def render_modify(self, record):
    link = '<center><a class="btn btn-danger btn-sm" href="/members/list/{}/"><span class="glyphicon glyphicon-pencil"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)


  class Meta:
    model = Member
    fields = ( 'id', 'type', 'member', 'head_of_list', 'status', 'users', 'details', 'modify', )
    attrs = {"class": "table"}


