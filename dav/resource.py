from djangodav.base.resources import MetaEtagMixIn
from djangodav.fs.resources import DummyFSDAVResource

from django.conf import settings

class MemberDavResource(MetaEtagMixIn, DummyFSDAVResource):
    root = '/var/www/clusil.lu/dav/members'

class BoardDavResource(MetaEtagMixIn, DummyFSDAVResource):
    root = '/var/www/clusil.lu/dav/board'
