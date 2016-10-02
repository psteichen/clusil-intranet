import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from django.template.loader import render_to_string
from django.conf import settings


################
# GLOBAL VIEWS #
################

def documentation(r):
  return render(r, settings.TEMPLATE_CONTENT['documentation']['template'], { 
			'title': settings.TEMPLATE_CONTENT['documentation']['title'], 
			'desc': settings.TEMPLATE_CONTENT['documentation']['desc'], 
			'docs': settings.TEMPLATE_CONTENT['documentation']['docs'], 
		})
# member home #
@login_required
def home(r):
  return render(r, settings.TEMPLATE_CONTENT['home']['template'], { 
			'title': settings.TEMPLATE_CONTENT['home']['title'], 
			'actions': settings.TEMPLATE_CONTENT['home']['actions'], 
		})

@permission_required('cms.SECR')
def board(r):
  return render(r, settings.TEMPLATE_CONTENT['board']['template'], { 
			'title': settings.TEMPLATE_CONTENT['board']['title'], 
			'actions': settings.TEMPLATE_CONTENT['board']['actions'], 
		})

