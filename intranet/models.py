from django.db import models

# this is only used to set custom permissions:
#
#  - clusil.BOARD	(member of the Management Board)
#  - clusil.SECR	(secretary of the Management Board)
#  - clusil.MEMBER	(CLUSIL member (for organisations only head-of-list and delegate get this permission))
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

