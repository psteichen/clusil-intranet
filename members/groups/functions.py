

def gen_group_initial(g):
  initial_data = {}

  initial_data['acronym'] = g.acronym
  initial_data['title'] = g.title
  initial_data['desc'] = g.desc
  initial_data['type'] = g.type
  initial_data['status'] = g.status

  return initial_data

