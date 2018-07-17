from django.conf import settings

def template_content(request):
    return settings.TEMPLATE_CONTENT

def group_perms(request):
  from django.contrib.auth.models import Group

  if request.user.is_authenticated():
    gl = request.user.groups.all().values_list('name', flat=True)
  else:
    gl = False
  if request.user.is_superuser: gl = Group.objects.all().values_list('name', flat=True)


  return  {
    'groups': gl,
  }

def user_context(request):
  from members.functions import is_hol, is_board, is_admin

  return {
    'is_hol': is_hol(request.user),
    'is_board': is_board(request.user),
    'is_admin': is_admin(request.user),
  }
