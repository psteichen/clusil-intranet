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

  return {
    'groups': gl
  }

