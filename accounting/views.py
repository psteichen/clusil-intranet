#coding=utf-8

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission

from django_tables2 import RequestConfig

from members.models import Member

from .models import Fee
from .tables import InvoiceTable
from .forms import PaymentForm

####################
# ACCOUNTING VIEWS #
####################

# list #
#########
@permission_required('cms.BOARD')
def list(request):
  request.breadcrumbs( ( ('board','/board/'),
                         ('treasury','/accounting/'),
                        ) )

  table = InvoiceTable(Fee.objects.all().order_by('-year'))
  RequestConfig(request, paginate={"per_page": 75}).configure(table)

  return render(request, settings.TEMPLATE_CONTENT['accounting']['template'], {
                        'title': settings.TEMPLATE_CONTENT['accounting']['title'],
#                        'actions': settings.TEMPLATE_CONTENT['accounting']['actions']['main'],
                        'table': table,
                        })


# validate payment #
####################
@permission_required('cms.BOARD')
def payment(r,member_id):
  r.breadcrumbs( ( 	
			('home','/'),
                   	('accounting','/accounting/'),
               ) )

  M = Member.objects.get(id=member_id)

  template 	= settings.TEMPLATE_CONTENT['accounting']['payment']['template']
  title 	= settings.TEMPLATE_CONTENT['accounting']['payment']['title']

  done_template = settings.TEMPLATE_CONTENT['accounting']['payment']['done']['template']
  done_title 	= settings.TEMPLATE_CONTENT['accounting']['payment']['done']['title']

  if r.POST:
    pf = PaymentForm(r.POST)
    if pf.is_valid():
      F = pf.save()

      # done 
      return render(r, done_template, {
			'title'		: done_title, 
                })

    else:
      # error in form -> show messages
      return render(r, done_template, {
                	'title'		: done_title, 
                	'error_message'	: settings.TEMPLATE_CONTENT['error']['gen'] + ' ; '.join([e for e in pf['who']]),
                })
    
  else:
    # no data yet -> empty form
    form = PaymentForm()
    return render(r, template, {
			'title'	: title, 
                	'form'	: form,
                 })


# invoice #
###########
@permission_required('cms.BOARD')
def invoice(r,member):
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('accounting','/accounting/'),
               ) )

  M = Member.objects.get(pk=member)

  template = settings.TEMPLATE_CONTENT['accounting']['invoice']['template']
  title = settings.TEMPLATE_CONTENT['accounting']['invoice']['title'].format(id=M.id)
  message = settings.TEMPLATE_CONTENT['accounting']['invoice']['message'].format(head=gen_fullname(M.head_of_list),year=date.today().strftime('%Y'))

  generate_invoice(M)

  return render(r, template, {
			'title'		: title,
			'message'	: message,
	       })


