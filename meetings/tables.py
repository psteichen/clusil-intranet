# coding=utf-8

from datetime import date

from django.utils.safestring import mark_safe
from django.utils.html import escape

from django_tables2.tables import Table
from django_tables2 import Column

from attendance.models import Meeting_Attendance
from members.models import Member

from .models import Meeting, Invitation

#table for visualisation via django_tables2
class MeetingTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Present/Excused',empty_values=())
  details	= Column(verbose_name='Details',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Meeting_Attendance.objects.filter(meeting=record,present=True).count(),Meeting_Attendance.objects.filter(meeting=record,present=False).count())

  def render_details(self, record):
    link = '<center><a class="btn btn-info btn-sm" href="/meetings/list/{}/"><span class="glyphicon glyphicon-list"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'location', 'totals', 'details', )
    attrs = {"class": "table table-striped"}

class MgmtMeetingTable(Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  totals	= Column(verbose_name='Present/Excused',empty_values=())
  details	= Column(verbose_name='Details',empty_values=())
  send		= Column(verbose_name='Invitations',empty_values=())
  modify	= Column(verbose_name='Modify',empty_values=())
  report	= Column(verbose_name='Minutes',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_totals(self, record):
    return '{} / {}'.format(Meeting_Attendance.objects.filter(meeting=record,present=True).count(),Meeting_Attendance.objects.filter(meeting=record,present=False).count())

  def render_details(self, record):
    link = '<center><a class="btn btn-info btn-sm" href="/meetings/list/{}/"><span class="glyphicon glyphicon-list"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  def render_send(self, record):
    sent = None
    try:
      I = Invitation.objects.get(meeting=record)
      sent = I.sent
    except: pass
    if sent: #already sent, resend?
      link = '<center><a class="btn btn-success btn-sm" href="/meetings/send/{}/" title="Renvoyer"><span class="glyphicon glyphicon-envelope"></span></a></center>'.format(escape(record.id))
    else: #not yet sent
      link = '<center><a class="btn btn-danger btn-sm" href="/meetings/send/{}/" title="Envoyer"><span class="glyphicon glyphicon-envelope"></span></a></center>'.format(escape(record.id))

    return mark_safe(link)

  def render_modify(self, record):
    link = '<center><a class="btn btn-danger btn-sm" href="/meetings/modify/{}/"><span class="glyphicon glyphicon-pencil"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  def render_report(self, record):
    if record.report: #report exists, resubmit?
      link = '<center><a class="btn btn-success btn-sm" href="/meetings/report/{}/" title="Resoumettre"><span class="glyphicon glyphicon-file"></span></a></center>'.format(escape(record.id))
    else: #submit report
      link = '<center><a class="btn btn-danger btn-sm" href="/meetings/report/{}/" title="Soumettre"><span class="glyphicon glyphicon-file"></span></a></center>'.format(escape(record.id))
    return mark_safe(link)

  class Meta:
    model = Meeting
    fields = ( 'title', 'when', 'location', 'totals', 'details', 'send', 'modify', 'report', )
    attrs = {"class": "table table-striped"}


class MeetingMixin(Table):
  present	= Column(verbose_name=u'Présent',empty_values=())
  excused	= Column(verbose_name=u'Excusé',empty_values=())
  nonexcused	= Column(verbose_name=u'Non-excusé',empty_values=())
  outside	= Column(verbose_name=u'Visite hors club',empty_values=())

  class Meta:
    model = Meeting
    fields = ( 'present', 'excused', 'oustide', 'non-excused', )

class MeetingListingTable(MeetingMixin, Table):
  row_class	= Column(visible=False, empty_values=()) #used to highlight some rows
  name		= Column(verbose_name=u'Nom (rôle)',empty_values=())
  email		= Column(verbose_name=u'E-mail',empty_values=())

  def render_row_class(self, record):
    if record.when < date.today():
      return 'danger'

  def render_name(self, record):
    return record.last_name + ' ' + record.first_name + '( ' + record.role.title + ')'

  def render_present(self, record):
    try:
      if Meeting_Attendance.objects.filter(meeting=record.id,member=record).only(present):
        return 'X'
    except: pass

  def render_excused(self, record):
    try:
      if not Meeting_Attendance.objects.filter(meeting=record.id,member=record).only(present):
        return 'X'
    except: pass

  def render_nonexcused(self, record):
    try:
      Meeting_Attendance.objects.filter(meeting=record.id,member=record).only(present)
    except:
      return 'X'

  class Meta:
    model = Member
    fields = ( 'name', 'present', 'excused', 'non-excused', 'outside', 'email', )
    attrs = {"class": "table table-striped"}

