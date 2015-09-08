# coding=utf-8
"""
Django settings for cms project.

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

ALLOWED_HOSTS = [ 'cms.clusil.lu', 'intranet.clusil.lu', ]

# Application definition

INSTALLED_APPS = (
# global bootstrap3 integration
  'bootstrap3',
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
# my apps
  'cms',
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
  'cms.context_processors.template_content',
)

ROOT_URLCONF = 'cms.urls'

WSGI_APPLICATION = 'cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'cms/db.sqlite'),
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
    os.path.join(BASE_DIR, 'cms/static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# LOCAL settings

#login/auth (used by the login_required decorator)
LOGIN_URL="/login/"
LOGIN_REDIRECT_URL="/home/"

#where to find templates
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'cms/templates/'),
  os.path.join(BASE_DIR, 'cms/templates/email/'),
  os.path.join(BASE_DIR, 'cms/templates/documentation/'),
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
    'author'            : 'Pascal Steichen - pst@clusil.lu ; 2012, 2014, 2015',
    'copyright'         : 'CLUSIL a.s.b.l. - info@clusil.lu ; 2012, 2014, 2015',
    'title'             : 'Club Management System',
    'logo' : {
      'url'		: "/",
      'img'		: 'http://clusil.lu/pics/clusil_picto.png',
    },
    'description'       : '',
    'keywords'          : '',
    'css' : {
        'bt'            : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css',
        'bt_theme'      : 'https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css',
        'jumbotron'	: 'https://clusil.lu/css/jumbotron.css',
        'jt_narrow'	: 'https://clusil.lu/css/jumbotron-narrow.css',
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

# home
HOME_ACTIONS = (
  {
    'heading'		: 'Membership Management',
    'has_perms'		: 'cms.MEMBER',
    'actions' : (
      {         
        'label'         : 'Profile', 
        'glyphicon'     : 'glyphicon-home',
        'desc'          : 'Manage your Membership profile',
        'url'           : '/members/profile/',
        'has_perms'	: 'cms.MEMBER',
      },
      {         
        'label'         : 'Users', 
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Manage users and their access profile',
        'url'           : '/members/users/',
        'has_perms'	: 'cms.MEMBER',
      },
    ),
  },
  {
    'heading'		: 'Collaboration Tools',
    'actions' : (
      {         
        'label'         : 'Cloud', 
        'glyphicon'     : 'glyphicon-folder-open',
        'desc'          : 'Filesharing platform (SeaFile based)',
        'url'           : 'https://cloud.clusil.lu/',
      },
    ),
  },
  {
    'heading'   	: 'Board Console',
    'has_perms'		: 'cms.BOARD',
    'actions' : (
      {         
        'label'         : 'Dashboard', 
        'glyphicon'     : 'glyphicon-tasks',
        'desc'          : 'Club management tools and functions',
        'url'           : '/board/',
        'has_perms'	: 'cms.BOARD',
      },
    ),
  },
)

TEMPLATE_CONTENT['home'] = {
  'title'     	: 'What do you want to do today ?',
  'template'    : 'actions.html',
  'actions'     : HOME_ACTIONS,
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
      'ref'	: 'cloud',
      'title'	: 'HowTo use the (SeaFile) cloud-system for document sharing',
      'content'	: 'cloud.html',
    },
  ),
}

#registration
from registration.settings import *
TEMPLATE_CONTENT['reg'] = REGISTRATION_TMPL_CONTENT

#where to store and get user-uploaded files
MEDIA_ROOT = '/var/www/clusil.lu/cms/media/'

# board
BOARD_ACTIONS = (
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

TEMPLATE_CONTENT['board'] = {
  'title'     	: 'What do you want to do today ?',
  'template'    : 'actions.html',
  'actions'     : BOARD_ACTIONS,
}

#members
from members.settings import *
TEMPLATE_CONTENT['members'] = MEMBERS_TMPL_CONTENT
#groups
from members.groups.settings import *
TEMPLATE_CONTENT['groups'] = GROUPS_TMPL_CONTENT
#profile
from members.profile.settings import *
TEMPLATE_CONTENT['profile'] = PROFILE_TMPL_CONTENT

#meetings
from meetings.settings import *
TEMPLATE_CONTENT['meetings'] = MEETINGS_TMPL_CONTENT

MEETINGS_ATTENDANCE_URL = 'http://new.intranet.clusil.lu/meetings/attendance/'

#events
#from events.settings import *
#TEMPLATE_CONTENT['events'] = EVENTS_TMPL_CONTENT

EVENTS_ATTENDANCE_URL = 'http://new.intranet.clusil.lu/events/attendance/'

#accounting
from accounting.settings import *
TEMPLATE_CONTENT['accounting'] = ACCOUNTING_TMPL_CONTENT
INVOICE = {
  'logo'	: STATIC_URL + 'pics/logo.jpg',
  'currency' 	: 'EUR',
}
