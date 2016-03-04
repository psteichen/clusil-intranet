

def gen_group_initial(g):
  initial_data = {}

  initial_data['acronym'] = g.acronym
  initial_data['title'] = g.title
  initial_data['desc'] = g.desc
  initial_data['type'] = g.type
  initial_data['status'] = g.status

  return initial_data


def affiliate(u,g):
  from .models import Affiliation
  try:
    #check if affiliation exists
    a = Affiliation.objects.get(user=u,group=g)
  except Affiliation.DoesNotExist:
    #does not exist -> create new
    a = Affiliation(user=u,group=g)
    
  a.save()
  

def get_affiliations(u):
  from .models import Affiliation
  out='<ul class="list-group">'
  affils = Affiliation.objects.filter(user=u)
  for a in affils:
    out+='<li class="list-group-item">'+unicode(a.group)+'</li>'

  out+='</ul>'
  return out
  
