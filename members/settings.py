# Application settings for members app
# coding=utf-8

ACTIONS = {
  'main' : (
    {
      'label'		: 'Add Member',
      'icon'    	: 'plus',
      'grade'          	: 'success',
      'url'     	: '/reg/',
      'perms'		: 'Board',
    },
    {
      'label'		: 'Annual Renewal',
      'icon'    	: 'refresh',
      'grade'          	: 'warning',
      'url'     	: '/members/renew/',
      'perms'		: 'Board',
    },
  ),
  'details' : (
    {
      'label'		: 'Change Member',
      'icon'		: 'pencil',
      'grade'		: 'warning',
      'url'    		: '/members/modify/{}/',
      'perms'		: 'Board',
    },
    {
      'label'		: 'View Invoices',
      'icon'		: 'euro',
      'grade'		: 'info',
      'url'    		: '/members/invoice/{}/',
      'perms'		: 'Board',
    },
    {
      'label'		: 'Add User',
      'icon'		: 'plus',
      'grade'		: 'success',
      'url'		: '/members/adduser/{}/',
      'perms'		: 'Board',
    },
  ),
  'roles' : (
    { 
      'label'		: 'Add Role', 
      'icon'   		: 'plus',
      'grade'          	: 'success', 
      'url'           	: '/members/role/add/', 
      'perms'		: 'Board',
    },
  ),
  'groups'   : (
    { 
      'label'         	: 'Add Group', 
      'icon'     	: 'plus',
      'grade'         	: 'success', 
      'url'           	: '/members/groups/add/', 
      'perms'		: 'Board',
    },
  ),
}

MEMBERS_TMPL_CONTENT = {
  'title'       	: 'Member Management',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'renew': {
    'template'		: 'done.html',
    'title'     	: 'Membership renewal requests for {year} sent.',
    'email': {
      'template'	: 'renewal_request.txt',
      'title'     	: 'Request to renew your membership for {year}.',
    },
  },
  'details': {
    'template'  	: 'done.html',
    'overview' : {
      'template'	: 'overview_member_board.html',
      'actions'  	: ACTIONS['details'],
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
