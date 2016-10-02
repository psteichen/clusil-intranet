# -*- coding: utf-8 -*-
#
# functions to facilitate usage of the django_tables2 plugin
#
from datetime import date, datetime, time

from django.conf import settings
from django.template.loader import render_to_string

###############################
# TABLES SUPPORTING FUNCTIONS #
###############################
def gen_table_actions(actions,url_param):
  from django.utils.safestring import mark_safe
  from django.utils.html import escape

  buttons = '<div class="btn-group-vertical" role="group">'
  for a in actions:
    link = '<a class="btn btn-sm btn-{grade}" href="{url}"><span class="glyphicon glyphicon-{icon}"></span>&nbsp;&nbsp;{label}</a>'.format(grade=a['grade'],url=a['url'].format(escape(url_param)),icon=a['icon'],label=a['label'])
    buttons += link
  buttons += '</div>'
  return mark_safe(buttons)

