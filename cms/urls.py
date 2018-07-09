from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

#from password_reset.views import recover, recover_done, reset, reset_done

from .views import home, documentation

from .views import board

urlpatterns = [

  #front-office
  url(r'^$', home, name='home'),
  url(r'^home/$', home, name='home'),
  url(r'^documentation/', documentation, name='documentaion'),
  url(r'^reg/', include('registration.urls')),
  url(r'^upload/', include('upload.urls')),

  #login stuff
  url(r'^login/', auth_views.LoginView.as_view(template_name='auth.html'), name='login'),
  url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
  url(r'^pwd/change/', auth_views.PasswordChangeView.as_view(template_name='chgpwd.html', success_url='/pwd/chg/done/'), name='password_change'),
  url(r'^pwd/change/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='done/chgpwd.html'), name='password_change_done'),

  url(r'^pwd/recover/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
  url(r'^pwd/recover/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  url(r'^pwd/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
  url(r'^pwd/reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

#  url(r'^pwd/recover/$', recover, name='password_reset_recover'),
#  url(r'^pwd/recover/(?P<signature>.+)/$', recover_done, name='password_reset_sent'),
#  url(r'^pwd/reset/done/$', reset_done, name='password_reset_done'),
#  url(r'^pwd/reset/(?P<token>[\w:-]+)/$', reset, name='password_reset_reset'),

  #members back-office (members)
  url(r'^profile/', include('members.profile.urls')),
  url(r'^ideabox/', include('ideabox.urls')),

  #admin back-office (board)
  url(r'^board/', board, name='board'),

  url(r'^members/', include('members.urls')),
  url(r'^members/groups/', include('members.groups.urls')),
  url(r'^meetings/', include('meetings.urls')),
  url(r'^events/', include('events.urls')),
  url(r'^locations/', include('events.urls')),
  url(r'^attendance/', include('attendance.urls')),

  url(r'^accounting/', include('accounting.urls')),

#  url(r'^events/', include('events.urls')),


  #admin
  url(r'^admin/', include(admin.site.urls)),

]
#serving media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

