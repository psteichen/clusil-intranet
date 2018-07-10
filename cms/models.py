from django.db import models

# this is only used to set custom permissions:
#
#  - cms.BOARD	(member of the Management Board)
#  - cms.SECR	(secretary of the Management Board)
#  - cms.MEMBER	(CLUSIL member (for organisations only head-of-list and delegate get this permission))
#
# including a little hack so that we can use these sepcific
# permissions in a choices field for HR creation
# 

class User(models.Model):
  BOARD = 'BOARD'
  SECR 	= 'SECR'
  MEMBER = 'MEMBER'
  PERMISSIONS = (
      (BOARD 	, 'BOARD'),
      (SECR 	, 'SECR'),
      (MEMBER 	, 'MEMBER'),
  )

  class Meta:
    permissions = (
      ('BOARD' 		, 'Member of the Board'),
      ('SECR' 		, 'Secretary of the Board'),
      ('MEMBER'		, 'CLUSIL member'),
    )

  def get_affiliations(self):
    from groups.models import get_affiliations
    return get_affiliations(self)


#LDAP stuff
#from ldapdb.models.fields import CharField, DateField, ImageField, ListField, IntegerField, FloatField
#import ldapdb.models
#
#
#class LdapUser(ldapdb.models.Model):
#    """
#    Class for representing an LDAP user entry.
#    """
#    # LDAP meta-data
#    base_dn = "ou=users,dc=clusil,dc=lu"
#    object_classes = ['inetOrgPerson']
#
#    # inetOrgPerson
#    first_name = CharField(db_column='givenName')
#    last_name = CharField(db_column='sn')
#    email = CharField(db_column='mail')
#    username = CharField(db_column='cn', primary_key=True)
#    password = CharField(db_column='userPassword')
#
#    def __unicode__(self):
#        return u'cn='+self.username+','+self.base_dn
#
#class LdapGroup(ldapdb.models.Model):
#    """
#    Class for representing an LDAP group entry.
#    """
#    # LDAP meta-data
#    base_dn = "ou=groups,dc=clusil,dc=lu"
#    object_classes = ['groupOfNames']
#
#    # posixGroup attributes
#    name = CharField(db_column='cn', max_length=200, primary_key=True)
#    members = ListField(db_column='member')
#
#    def __unicode__(self):
#        return self.name
