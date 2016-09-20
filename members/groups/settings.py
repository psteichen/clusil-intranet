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
      'has_perms'     	: 'cms.SECR',
    },
  ),
  'list': ( 
    { 
      'label'    	: 'Modify Group', 
      'icon'     	: 'pencil',
      'grade'     	: 'danger',
      'desc'          	: 'Modify a Group', 
      'url'           	: '/members/groups/modify/', 
      'has_perms'     	: 'cms.SECR',
    },
  ),
  'affil': ( 
    { 
      'label'    	: 'Add User to Group', 
      'icon'     	: 'plus',
      'grade'     	: 'danger',
      'desc'    	: 'Add User to Group', 
      'url'           	: '/members/groups/adduser/{}/', 
      'has_perms'     	: 'cms.SECR'
    },
  ),
}

GROUPS_TMPL_CONTENT = {
  'title'       	: 'Group Management',
  'template'    	: 'list.html',
  'desc'     		: '''
	<p class="text-success">GREEN: <b>active groups</b></p>
	<p class="text-warning">AMBER: <b>standby/inactive groups</b></p>
	<p class="text-info">BLUE: <b>special groups</b></p>
	<p class="text-muted">WHITE: <b>old/archived groups</b></p>
''',
  'actions'     	: ACTIONS['main'],
  'list_actions'     	: ACTIONS['list'],
  'affil': {
    'template'		: 'done.html',
    'title'     	: 'Group affiliations for <i>{}</i>',
    'actions'     	: ACTIONS['affil'],
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
  'adduser': {
    'template'		: 'form.html',
    'title'     	: 'Affiliate User to Group {}',
    'desc'     		: '',
    'submit'   		: 'Add',
    'done' : {
      'template'        : 'done.html',
      'title'     	: 'Added User(s) to Group <i>{}</i>',
    },
  },
}
