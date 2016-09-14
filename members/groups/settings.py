# Application settings for groups app
# coding=utf-8

ACTIONS = {
  'main': ( 
    { 
      'label'         	: 'Add Group', 
      'icon'     	: 'plus',
      'grade'     	: 'danger',
      'desc'          	: 'Add a Group', 
      'url'           	: '/members/groups/add/', 
      'has_perms'     	: 'clusil.BOARD',
    },
  ),
  'list': ( 
    { 
      'label'    	: 'Modify Group', 
      'icon'     	: 'pencil',
      'grade'     	: 'danger',
      'desc'          	: 'Modify a Group', 
      'url'           	: '/members/groups/modify/', 
      'has_perms'     	: 'clusil.BOARD',
    },
  ),
}

GROUPS_TMPL_CONTENT = {
  'title'       	: 'Group Management',
  'template'    	: 'list.html',
  'desc'     		: '''
	<p class="text-success">GREEN: <b>active groups</b></p>
	<p class="text-warning">AMBER: <b>standby/inactive groups</b></p>
	<p class="text-muted">WHITE: <b>old/archived groups</b></p>
''',
  'actions'     	: ACTIONS['main'],
  'list_actions'     	: ACTIONS['list'],
  'affil': {
    'template'		: 'done.html',
    'title'     	: 'Group affiliations for <i>{}</i>',
    'overview' : {
      'template'	: 'overview_groups_affil.html',
    },
  },
  'add': {
    'template'		: 'form.html',
    'title'     	: 'Add Group',
    'desc'     		: '',
    'submit'   		: 'Add',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Group added.',
      'message'     	: 'Details here: ',
    },
  },
  'modify': {
    'template'		: 'form.html',
    'title'     	: 'Modify Group',
    'desc'     		: '',
    'submit'   		: 'Modify',
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Group [%s] modified!',
    },
  },
}
