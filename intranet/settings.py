# coding=utf-8
"""
Django settings for intranet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '"&_-L%/(OI&RBçtzdb*v6hv+b8@rav4fgh@zre64z$54wrefdB%&*/Ã§ZR(r!)0b71c1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [ 'new.intranet.clusil.lu', 'intranet.clusil.lu', ]

# Application definition

INSTALLED_APPS = (
# django core apps
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
# specific supporting apps
  'django_tables2',
  'breadcrumbs',
  'captcha',
  'password_reset',
# apps needed for django-wiki
  'django.contrib.sites',
  'django.contrib.humanize',
  'django_nyt',
#  'django_notify',
  'mptt',
  'sekizai',
  'sorl.thumbnail',
  'wiki',
  'wiki.plugins.attachments',
  'wiki.plugins.notifications',
  'wiki.plugins.images',
  'wiki.plugins.macros',
# webdav (djangodav based)
  'djangodav',
  'dav',
# my apps
  'intranet',
  'members',
  'members.groups',
  'meetings',
  'events',
  'webcontent',
)

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
# via supporting apps
  'breadcrumbs.middleware.BreadcrumbsMiddleware',
# force login for wiki
  'intranet.middleware.RequireLoginMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  'django.core.context_processors.tz',
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.request', #needed for django-tables2
  'django.core.context_processors.debug', #needed for django-wiki
  'sekizai.context_processors.sekizai', #needed for django-wiki
  'intranet.context_processors.template_content',
)

ROOT_URLCONF = 'intranet.urls'

WSGI_APPLICATION = 'intranet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'intranet/db.sqlite'),
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/Luxembourg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'intranet/static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# LOCAL settings

#login/auth (used by the login_required decorator)
LOGIN_URL="/login/"
LOGIN_REDIRECT_URL="/home/"
FORCE_LOGIN_URLS = (
  r'/wiki/(.*)$',
  r'/wiki/notifications/(.*)$',
)
LOGIN_REQUIRED_URLS_EXCEPTIONS = (
  r'/$',
)


#where to find templates
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'intranet/templates/'),
  os.path.join(BASE_DIR, 'intranet/templates/email/'),
  os.path.join(BASE_DIR, 'intranet/templates/documentation/'),
)

#ReCAPTCHA stuff
RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = "6LdpL9MSAAAAAOKQi8TiU0VF0F550yc7uSppQb9X"
RECAPTCHA_PRIVATE_KEY = "6LdpL9MSAAAAANJyK4IO7L5aCL8kyxNfh36sGXcs"

#emails
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'CLUSIL Admin <admin@clusil.lu>'

ADMINS = (
  ('Pascal Steichen', 'pst@clusil.lu'),
)

EMAILS = {
  'sender' : {
    'default'	: 'CLUSIL Board <board@clusil.lu>',
  },
  'footer' 	: '''
Best Regads,
Your CLUSIL team
''',
}

#content for templates and views
TEMPLATE_CONTENT = {
  #basic/generic content for all templates/views:
  'meta' : {
    'author'            : 'Pascal Steichen - pst@clusil.lu ; 2012, 2014',
    'copyright'         : 'CLUSIL a.s.b.l. - info@clusil.lu ; 2012, 2014',
    'title'             : 'CLUSIL INTRANET',
    'logo' : {
      'title'		: "",
      'img'		: 'http://clusil.lu/pics/clusil_picto.png',
    },
    'description'       : '',
    'keywords'          : '',
    'css' : {
        'bt'            : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css',
        'bt_theme'      : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css',
        'jumbotron'	: 'https://aperta.lu/css/jumbotron.css',
        'jt_narrow'	: 'https://aperta.lu/css/jumbotron-narrow.css',
        'own'           : STATIC_URL + 'css/bt-clusil.css',
    },
    'js' : {
        'bt'       	: 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js',
        'jq'		: 'https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js',
    },
  },
  'error' : {
    'gen'               : 'Error in input validation!',
    'email'             : 'Error in email notification!',
    'no-data'           : 'No data!',
    'duplicate'         : 'Duplicate found, reconsider your input!',
  },
  'auth' : {
    'title': 'Authentication',
    'submit': 'Login',
  },
  'pwd' : {
    'recover' : {
      'title': 'Password Recovery',
      'submit': 'Recover',
      'done' : {
        'title': 'Password Recovery completed successfully',
        'message': 'Your password has been changed successfully. Please re-login with your new credentials.',
      },
    },
    'change' : {
      'title': 'Change password for User: ',
      'submit': 'Change',
      'done' : {
        'title': 'Password Change completed successfully',
        'message': 'Your password has been changed successfully. Please re-login with your new credentials.',
        'backurl': '/',
        'backurl_txt': 'Back to main page.',
      },
    },
  },
}

# open_home
OPEN_ACTIONS = (
  {
    'heading'      : 'Registration and Documentation',
    'actions'   : (
      {         
        'label'         : 'Registration', 
        'glyphicon'     : 'glyphicon-ok',
        'desc'          : 'Register for CLUSIL membership (including Intranet access)',
        'url'           : '/reg/',
      },
      {         
        'label'         : 'Documentation', 
        'glyphicon'     : 'glyphicon-book',
        'desc'          : 'How to use the CLUSIL Intranet',
        'url'           : '/documentation/',
      },
    ),
  },
  {
    'heading'      : 'Collaboration Tools',
    'actions'   : (
      {         
        'label'         : 'WebDAV', 
        'glyphicon'     : 'glyphicon-folder-open',
        'desc'          : 'Filesharing platform (WebDAV based)',
        'url'           : '/dav/members/',
      },
      {         
        'label'         : 'Wiki', 
        'glyphicon'     : 'glyphicon-pencil',
        'desc'          : 'Collaboration platform (Wiki based)',
        'url'           : '/wiki/',
      },
    ),
  },

)

TEMPLATE_CONTENT['open_home'] = {
  'title'     	: 'What do you want to do today ?',
  'template'    : 'actions.html',
  'actions'     : OPEN_ACTIONS,
}

#documentation
TEMPLATE_CONTENT['documentation'] = {
  'title'     	: 'CLUSIL Intranet Documentation',
  'desc'     	: 'Use the categories/tabs herebelow to view the documentation on how to best use the CLUSIL Intranet:',
  'template'    : 'main.html',
  'docs' : (
    {
      'ref'	: 'reg',
      'title'	: 'HowTo register and use the membership platform',
      'content'	: 'reg.html',
    },
    {
      'ref'	: 'dav',
      'title'	: 'HowTo use the (WebDAV) filesystem for document sharing',
      'content'	: 'dav.html',
    },
    {
      'ref'	: 'wiki',
      'title'	: 'HowTo use the Wiki for collaboration',
      'content'	: 'wiki.html',
    },
  ),
}

#registration
from registration.settings import *
TEMPLATE_CONTENT['reg'] = REGISTRATION_TMPL_CONTENT

#where to store and get user-uploaded files
MEDIA_ROOT = '/var/www/clusil.lu/dav/'

# home
ACTIONS = (
  {
    'heading'      	: 'Web and online content management applications:',
    'actions' : (
      {         
        'label'         : 'Web Content Management', 
        'glyphicon'     : 'glyphicon-cloud',
        'desc'          : 'Manage the public website content',
        'url'           : '/webcontent/',
      },
      {         
        'label'         : 'Event Management', 
        'glyphicon'     : 'glyphicon-glass',
        'desc'          : 'Manage special events or activities',
        'url'           : '/events/',
      },

    ),
  },
  {
    'heading'      	: 'Admin and internal management applications:',
    'actions' : (
      {         
        'label'         : 'Meeting Management', 
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Manage regular meetings (board working groups...)',
        'url'           : '/meetings/',
      },
      {         
        'label'         : 'Member Management', 
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Manage members',
        'url'           : '/members/',
      },
    ),
  },
)

TEMPLATE_CONTENT['home'] = {
  'title'     	: 'What do you want to do today ?',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
}

#members
from members.settings import *
TEMPLATE_CONTENT['members'] = MEMBERS_TMPL_CONTENT
#groups
from members.groups.settings import *
TEMPLATE_CONTENT['groups'] = GROUPS_TMPL_CONTENT

#meetings
from meetings.settings import *
TEMPLATE_CONTENT['meetings'] = MEETINGS_TMPL_CONTENT

MEETINGS_ATTENDANCE_URL = 'http://intranet.clusil.lu/meetings/attendance/'

#dav
from dav.settings import *
TEMPLATE_CONTENT['dav'] = DAV_TMPL_CONTENT

#events
#from events.settings import *
#TEMPLATE_CONTENT['events'] = EVENTS_TMPL_CONTENT

EVENTS_ATTENDANCE_URL = 'http://intranet.clusil.lu/events/attendance/'

#webcontent
#from webcontent.settings import *
#TEMPLATE_CONTENT['webcontent'] = WEBCONTENT_TMPL_CONTENT

#wiki settings
SITE_ID = 1 
WIKI_ACCOUNT_SIGNUP_ALLOWED=False

