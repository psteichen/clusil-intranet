#coding=utf-8

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.forms.models import model_to_dict

from django_tables2 import RequestConfig

from members.functions import gen_fullname
from members.models import Member

from .models import Fee
from .tables import InvoiceTable
from .forms import PaymentForm
from .functions import generate_invoice, generate_credit_note

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
def payment(r,member_id,year):
  r.breadcrumbs( ( 	
			('home','/'),
                   	('accounting','/accounting/'),
               ) )

  M = Member.objects.get(id=member_id)
  F = Fee.objects.get(member=member_id,year=year)

  template 	= settings.TEMPLATE_CONTENT['accounting']['payment']['template']
  title 	= settings.TEMPLATE_CONTENT['accounting']['payment']['title']
  submit 	= settings.TEMPLATE_CONTENT['accounting']['payment']['submit']

  done_template = settings.TEMPLATE_CONTENT['accounting']['payment']['done']['template']
  done_title 	= settings.TEMPLATE_CONTENT['accounting']['payment']['done']['title']

  if r.POST:
    pf = PaymentForm(r.POST, instance=F)
    if pf.is_valid():
      fee = pf.save(commit=False)
      fee.paid = True
      fee.save()

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
    form.initial= model_to_dict(F)
    form.instance = F
    return render(r, template, {
			'title'		: title, 
                	'form'		: form,
                	'submit'	: submit,
                 })


# invoice #
###########
@permission_required('cms.BOARD')
def invoice(r,member,year):
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('accounting','/accounting/'),
               ) )

  M = Member.objects.get(pk=member)

  template = settings.TEMPLATE_CONTENT['accounting']['invoice']['template']
  title = settings.TEMPLATE_CONTENT['accounting']['invoice']['title'].format(id=M.id)
  message = settings.TEMPLATE_CONTENT['accounting']['invoice']['message'].format(member=M,year=year,head=gen_fullname(M.head_of_list))

  # generate invoice and sent to head-of-list
  generate_invoice(M,year)

  return render(r, template, {
			'title'		: title,
			'message'	: message,
	       })

# credit #
##########
@permission_required('cms.BOARD')
def credit(r,member,year): #year is not used, but for sake of easiness keep it
  r.breadcrumbs( ( 
			('home','/home/'),
                       	('accounting','/accounting/'),
               ) )

  M = Member.objects.get(pk=member)

  template = settings.TEMPLATE_CONTENT['accounting']['credit']['template']
  title = settings.TEMPLATE_CONTENT['accounting']['credit']['title'].format(id=M.id)
  message = settings.TEMPLATE_CONTENT['accounting']['credit']['message'].format(member=M,year=year,head=gen_fullname(M.head_of_list))

  # generate credit note and sent to head-of-list
  generate_credit_note(M)

  return render(r, template, {
			'title'		: title,
			'message'	: message,
	       })


