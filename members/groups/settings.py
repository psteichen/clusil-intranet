# Application settings for groups app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choose actions on <strong>groups</strong>:',
    'has_perms'         : 'clusil.BOARD',
    'actions'   : (
      { 
        'label'         : 'Add Group', 
        'glyphicon'     : 'glyphicon-th-large',
        'desc'          : 'Add a Group', 
        'url'           : '/members/groups/add/', 
	'has_perms'     : 'clusil.BOARD',
      },
      { 
        'label'         : 'Modify Group', 
        'glyphicon'     : 'glyphicon-th-large',
        'desc'          : 'Modify a Group', 
        'url'           : '/members/groups/modify/', 
	'has_perms'     : 'clusil.BOARD',
      },

      { 
        'label'         : 'List Groups', 
        'glyphicon'     : 'glyphicon-th-large',
        'desc'          : 'List all groups', 
        'url'           : '/members/groups/list/', 
	'has_perms'     : 'clusil.BOARD',
      },

    ),
  },
)

GROUPS_TMPL_CONTENT = {
  'title'       	: 'Group Management',
  'template'    	: 'actions.html',
  'actions'     	: ACTIONS,
  'add': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][0]['desc'],
    'desc'     		: '',
    'submit'   		: 'Add Group',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Group added.',
      'message'     	: 'Details here: ',
    },
  },
  'modify': {
    'title'     	: ACTIONS[0]['actions'][1]['desc'],
    'overview' : {
      'title'           : 'Overview',
    },
    'list' : {
      'title'           : 'Choose Group to modify',
      'next'            : 'next',
    },
    'group' : {
      'title'           : 'Modify Group',
      'next'            : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Group [%s] modified!',
    },
  },
  'list': {
    'template'  	: 'list.html',
    'title'     	: ACTIONS[0]['actions'][1]['label'],
    'desc'     		: 'GREEN: active groups<br/>AMBER: standby/inactive groups<br/>WHITE: old/archived groups',
  },
}
