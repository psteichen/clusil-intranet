# Application settings for members app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: 'Add Member',
      'icon'    	: 'plus',
      'grade'          	: 'success',
      'url'     	: '/reg/',
      'has_perms'	: 'cms.SECR',
    },
    {
      'label' 	        : 'Group management',
      'icon'  	   	: 'th-large',
      'grade'    	: 'info',
      'url'           	: '/members/groups/',
      'has_perms'	: 'cms.SECR',
    },
  ),
  'details' : (
    {
      'label'	: 'Change Member',
      'icon'	: 'pencil',
      'grade'	: 'warning',
      'url'    	: '/profile/modify/',
    },
    {
      'label'	: 'View Invoices',
      'icon'	: 'euro',
      'grade'	: 'info',
      'url'    	: '/profile/invoice/',
    },
    {
      'label'	: 'Add User',
      'icon'	: 'plus',
      'grade'	: 'success',
      'url'	: '/profile/adduser/',
    },
  ),
  'roles' : (
    { 
      'label'		: 'Add Role', 
      'icon'   		: 'plus',
      'grade'          	: 'success', 
      'url'           	: '/members/role/add/', 
      'has_perms'	: 'cms.SECR',
    },
  ),
  'groups'   : (
    { 
      'label'         	: 'Add Group', 
      'icon'     	: 'plus',
      'grade'         	: 'success', 
      'url'           	: '/members/groups/add/', 
      'has_perms'	: 'cms.SECR',
    },
  ),
}

MEMBERS_TMPL_CONTENT = {
  'title'       	: 'Member Management',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: 'Add Member',
    'desc'     		: '',
    'submit'   		: 'Add Member',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Member added.',
      'message'     	: 'Details here: ',
    },
  },
  'details': {
    'template'  	: 'done.html',
    'overview' : {
      'template'	: 'overview_member.html',
      'actions'     	: ACTIONS['details'],
    },
    'readonly' : {
      'template'	: 'overview_member_readonly.html',
    },
  },
  'modify': {
    'title'     	: 'Modify member profile',
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
  'role' : {
    'add': {
      'template'	: 'form.html',
      'title'     	: 'Add Role',
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
