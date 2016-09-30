from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from password_reset.views import recover, recover_done, reset, reset_done

from .views import home, documentation

from .views import board

urlpatterns = patterns('',

  #front-office
  url(r'^$', home, name='home'),
  url(r'^home/$', home, name='home'),
  url(r'^documentation/', documentation, name='documentaion'),
  url(r'^reg/', include('registration.urls')),
  url(r'^upload/', include('upload.urls')),

  #login stuff
  url(r'^login/', 'django.contrib.auth.views.login', {'template_name': 'auth.html'}, name='login'),
  url(r'^logout/', 'django.contrib.auth.views.logout_then_login', name='logout'),
  url(r'^pwd/change/', 'django.contrib.auth.views.password_change', {'template_name': 'chgpwd.html', 'post_change_redirect': '/pwd/chg/done/'}, name='password_change'),
  url(r'^pwd/change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'done/chgpwd.html'}, name='password_change_done'),
  url(r'^pwd/recover/$', recover, name='password_reset_recover'),
  url(r'^pwd/recover/(?P<signature>.+)/$', recover_done, name='password_reset_sent'),
  url(r'^pwd/reset/done/$', reset_done, name='password_reset_done'),
  url(r'^pwd/reset/(?P<token>[\w:-]+)/$', reset, name='password_reset_reset'),

  #members back-office (members)
  url(r'^profile/', include('members.profile.urls')),

  #admin back-office (board)
  url(r'^board/', board, name='board'),

  url(r'^members/', include('members.urls')),
  url(r'^members/groups/', include('members.groups.urls')),
  url(r'^meetings/', include('meetings.urls')),
  url(r'^events/', include('events.urls')),
  url(r'^locations/', include('events.urls')),

  url(r'^accounting/', include('accounting.urls')),

#  url(r'^events/', include('events.urls')),

#  url(r'^webcontent/', include('webcontent.urls')),

  #admin
  url(r'^admin/', include(admin.site.urls)),

)
#serving media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

