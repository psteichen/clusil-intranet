import datetime

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required, permission_required

from django.template.loader import render_to_string
from django.conf import settings

from cms.functions import group_required

################
# GLOBAL VIEWS #
################

def documentation(r):
  return TemplateResponser(r, settings.TEMPLATE_CONTENT['documentation']['template'], { 
				'title': settings.TEMPLATE_CONTENT['documentation']['title'], 
				'desc': settings.TEMPLATE_CONTENT['documentation']['desc'], 
				'docs': settings.TEMPLATE_CONTENT['documentation']['docs'], 
			  })

# member home #
@group_required('MEMBER')
def home(r):
  return TemplateResponse(r, settings.TEMPLATE_CONTENT['home']['template'], { 
				'title': settings.TEMPLATE_CONTENT['home']['title'], 
				'actions': settings.TEMPLATE_CONTENT['home']['actions'], 
			 })

@group_required('BOARD')
def board(r):
  r.breadcrumbs( ( 
			('board','/board/'),
               ) )


  return TemplateResponse(r, settings.TEMPLATE_CONTENT['board']['template'], { 
				'title': settings.TEMPLATE_CONTENT['board']['title'], 
				'actions': settings.TEMPLATE_CONTENT['board']['actions'], 
			 })

