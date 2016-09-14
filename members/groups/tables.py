#coding=utf-8

from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from members.models import Member
from .models import Group, Affiliation

#table for visualisation via django_tables2
class GroupTable(Table):
  row_class     = Column(visible=False, empty_values=()) #used to highlight some rows
  involvement	= Column(empty_values=())
  actions	= Column(empty_values=())

  def render_row_class(self, value, record):
    if record.status == Group.STB:
      return 'info'

    if record.status == Group.ACT:
      return 'success'

    if record.status == Group.OLD:
      return 'muted'

  def render_involvement(self, value, record):
    count = Affiliation.objects.filter(group=record.pk).count()
    link = '<a class="btn btn-sm btn-default" href="/members/groups/affil/'+escape(record.pk)+'/">'+escape(count)+'</a>'
    return mark_safe(link)

  def render_actions(self, value, record):
    link = '<center>'
    for a in settings.TEMPLATE_CONTENT['groups']['list_actions']:
      link += '<a class="btn btn-sm btn-'+a['grade']+'" href="'+a['url']+escape(record.pk)+'/"><span class="glyphicon glyphicon-'+a['icon']+'"></span></a>'
    link += '</center>'
    return mark_safe(link)

  class Meta:
    model = Group
    fields = ( 'type', 'acronym', 'title', 'desc', 'involvement', 'actions', )
    attrs = {"class": "table"}

