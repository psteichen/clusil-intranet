# Application settings for members app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choose actions on <strong>members</strong>:',
    'has_perms'		: 'clusil.SECR',
    'actions'   : (
      {
        'label'         : 'Add Member',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Add a new member',
        'url'           : '/members/add/',
        'has_perms'	: 'clusil.SECR',
      },
      {
        'label'         : 'Modify Member',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Modify member',
        'url'           : '/members/modify/',
        'has_perms'	: 'clusil.SECR',
      },
      {
        'label'         : 'List Members',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'List all members',
        'url'           : '/members/list/',
        'has_perms'	: 'clusil.SECR',
      },
    ),
  },
  {
    'heading'           : 'Choose actions on <strong>roles</strong>:',
    'has_perms'		: 'clusil.SECR',
    'actions'   : (
      { 
        'label'         : 'Add Role', 
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Add a Member Role', 
        'url'           : '/members/role/add/', 
        'has_perms'	: 'clusil.SECR',
      },
     ),
  },
  {
    'heading'           : 'Group management',
    'has_perms'         : 'clusil.BOARD',
    'actions'   : (
      { 
        'label'         : 'Group Management', 
        'glyphicon'     : 'glyphicon-th-large',
        'desc'          : 'Manage Groups', 
        'url'           : '/members/groups/', 
        'has_perms'	: 'clusil.BOARD',
      },
    ),
  },
)

MEMBERS_TMPL_CONTENT = {
  'title'       	: 'Member Management',
  'template'    	: 'actions.html',
  'actions'     	: ACTIONS,
  'add': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][0]['desc'],
    'desc'     		: '',
    'submit'   		: 'Add Member',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Member added.',
      'message'     	: 'Details here: ',
    },
  },
  'profile': {
    'template'          : 'done.html',
#    'actions'           : ACTIONS['profile'],
    'title'             : u'User profile',
    'overview' : {
      'template'        : 'overview_member.html',
      'name'            : u'Nom',
      'username'        : u'Login',
      'email'           : u'E-mail',
      'role'            : u'Rôle',
    },
  },
  'modify': {
    'title'     	: ACTIONS[0]['actions'][1]['desc'],
    'first'             : 'first',
    'prev'              : 'back',
    'overview' : {
      'title'           : 'Overview',
    },
    'list' : {
      'title'           : 'Choose Member to modify',
      'next'            : 'next',
    },
    'member' : {
      'title'           : 'Modify Member',
      'next'            : 'submit',
    },
    'role' : {
      'title'           : 'Modify Role',
      'next'            : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Member [%s] modified!',
    },
  },
  'list': {
    'template'  : 'list.html',
    'title'     : 'List of Members',
    'desc'     	: '',
  },
  'role' : {
    'add': {
      'template'	: 'form.html',
      'title'     	: ACTIONS[1]['actions'][0]['desc'],
      'desc'     	: '',
      'submit'   	: 'Add Member Role',
      'done': {
        'template'	: 'done.html',
        'title'     	: 'New Member Role added.',
        'message'     	: 'Details here: ',
      },
    },
  },
}
