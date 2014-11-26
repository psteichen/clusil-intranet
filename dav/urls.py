from djangodav.acls import FullAcl
from djangodav.locks import DummyLock
from djangodav.views import DavView

from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import patterns, url

from .resource import MemberDavResource, BoardDavResource
from .views import upload

#member dav view
member_dav_view = DavView.as_view(resource_class=MemberDavResource, lock_class=DummyLock, acl_class=FullAcl)
#wrapper with specific permissions
member_dav_view_wrapper = login_required(member_dav_view)

#board dav view
board_dav_view = DavView.as_view(resource_class=BoardDavResource, lock_class=DummyLock, acl_class=FullAcl)
#wrapper with specific permissions
board_dav_view_wrapper = permission_required('clusil.BOARD')(board_dav_view)



urlpatterns = patterns('',
  url(r'^members/(?P<path>.*)$', member_dav_view_wrapper, name="member-dav" ),
  url(r'^board/(?P<path>.*)$', board_dav_view_wrapper, name="board-dav" ),
  url(r'^upload/(?P<path>.*)$', upload, name="upload" ),
)
