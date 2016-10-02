from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission

from django_tables2 import RequestConfig

from .models import Fee
from .tables import InvoiceTable
from .forms import FeeForm

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
                        'actions': settings.TEMPLATE_CONTENT['accounting']['actions'],
                        'table': table,
                        })


# payment function #
####################
@permission_required('cms.BOARD')
def payment(r):
  if r.POST:
    payments=r.POST.getlist('payments')
    msg="""
The following Members have payed:
"""
    for p in payments:
      try:
        m = Member.objects.get(member_id=p)
        f = Fee(member=m)
        f.paid = True
        f.save()

        #add to payed list
        msg+="""  > """ + m.member_id + """ (""" + m.user.first_name + """ """ + unicode.upper(m.user.last_name) + """) <
"""
      except Member.DoesNotExist:
        return render(r,'board.html', {'title': 'Validate membership fee payments','form': FeeForm(), 'error_message': settings.TEMPLATE_CONTENT['error']['board']})

    return render(r,'done.html', {'mode': 'validating payments', 'message': msg})
  else:
   #no POST data yet -> show profile form
   return render(r,'board.html', {'title': 'Validate membership fee payments','form': FeeForm(),})

