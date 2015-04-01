from django.db.models import Model, IntegerField, CharField, ForeignKey
from django.contrib.auth.models import User

from members.functions import gen_fullname

# Group (board, working group, etc.) model
class Group(Model):
  MG = 0
  WG = 1
  AG = 2
  TYPES = (
    (MG, 'Management Group'), #only for specific members
    (WG, 'Working Group'),
    (AG, 'Ad-Hoc Group'),
  )

  ACT = 0
  STB = 1
  OLD = 2
  STATUSES = (
    (ACT, 'active'),
    (STB, 'standby'), #inactive
    (OLD, 'archived'), #not used any more
  )

  acronym 	= CharField(max_length=15,primary_key=True)
  title 	= CharField(max_length=150)
  desc 		= CharField(max_length=500,blank=True,null=True)
  type 		= IntegerField(choices=TYPES)
  status      	= IntegerField(choices=STATUSES,default=ACT) 

  def __unicode__(self):
    return '[' + self.TYPES[self.type][1] +'] ' + unicode.upper(self.acronym) + ' - ' + self.title


# Affiliation (user to group) model
class Affiliation(Model):
  user 		= ForeignKey(User)
  group 	= ForeignKey(Group)

  def __unicode__(self):
    g=u' - '
    try:
      g = self.group.acronym
    except: pass
    return gen_fullname(self.user) + unicode.upper(g)

  class Meta:
    unique_together = ( 'user', 'group', )


