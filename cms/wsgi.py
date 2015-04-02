"""
WSGI config for cms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys

# set sys.path to the directory containing the django app
# else wsgi will not find the settings file below
sys.path.append('/var/www/clusil.lu/django')
sys.path.append('/var/www/clusil.lu/django/cms')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
