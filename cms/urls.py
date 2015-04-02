from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

from password_reset.views import recover, recover_done, reset, reset_done

from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


from .views import home, documentation

from .views import board

urlpatterns = patterns('',

  #front-office
  url(r'^$', home, name='home'),
  url(r'^home/$', home, name='home'),
  url(r'^documentation/', documentation, name='documentaion'),

  url(r'^reg/', include('registration.urls')),

  #wiki
  url(r'^wiki/notifications/', get_nyt_pattern()),
  url(r'^wiki/', get_wiki_pattern()),


  #login stuff
  url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'auth.html'}, name='login'),
  url(r'^logout/', 'django.contrib.auth.views.logout_then_login', name='logout'),
  url(r'^pwd/change/', 'django.contrib.auth.views.password_change', {'template_name': 'chgpwd.html', 'post_change_redirect': '/pwd/chg/done/'}, name='password_change'),
  url(r'^pwd/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'done/chgpwd.html'}, name='password_change_done'),
  url(r'^pwd/recover/$', recover, name='password_reset_recover'),
  url(r'^pwd/recover/(?P<signature>.+)/$', recover_done, name='password_reset_sent'),
  url(r'^pwd/reset/done/$', reset_done, name='password_reset_done'),
  url(r'^pwd/reset/(?P<token>[\w:-]+)/$', reset, name='password_reset_reset'),


  #back-office
  url(r'^board/', board, name='board'),

  url(r'^members/', include('members.urls')),
  url(r'^members/groups/', include('members.groups.urls')),
  url(r'^profile/', include('members.profile.urls')),

  url(r'^meetings/', include('meetings.urls')),

  url(r'^accounting/', include('accounting.urls')),

#  url(r'^events/', include('events.urls')),

#  url(r'^webcontent/', include('webcontent.urls')),

  url(r'^dav/', include('dav.urls')),

  #admin
  url(r'^admin/', include(admin.site.urls)),

)
