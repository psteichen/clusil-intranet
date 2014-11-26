from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission

from .forms import FeeForm

####################
# ACCOUNTING VIEWS #
####################
@permission_required('clusil.BOARD')
def index(r):
  return render(r, 'actions.html', {'action_list': settings.TEMPLATE_CONTENT['accounting']['action_list']})


# payment function #
####################
@permission_required('clusil.BOARD')
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

