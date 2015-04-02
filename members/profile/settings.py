# Application settings for profile app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Membership profile',
    'has_perms'         : 'cms.MEMBER',
    'actions'   : (
      {
        'label'         : 'Modify Profile',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Modify, adjust Membership profile',
        'url'           : '/profile/modify/',
    	'has_perms'     : 'cms.MEMBER',
      },
      {
        'label'         : 'Add User',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Add a User to your membership',
        'url'           : '/profile/adduser/',
    	'has_perms'     : 'cms.MEMBER',
      },
      {
        'label'         : 'Delete User',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Delete a User from your membership',
        'url'           : '/profile/tiltuser/',
    	'has_perms'     : 'cms.MEMBER',
      },
      {
        'label'         : 'Change Head-of-list',
        'glyphicon'     : 'glyphicon-user',
        'desc'          : 'Change Head-of-list or Delegate for your membership',
        'url'           : '/profile/chg_hol_d/',
    	'has_perms'     : 'cms.MEMBER',
      },
      {
        'label'         : 'Invoice',
        'glyphicon'     : 'glyphicon-euro',
        'desc'          : 'View invoice(s) from your membership',
        'url'           : '/profile/invoice/',
    	'has_perms'     : 'cms.MEMBER',
      },
    ),
  },
)

PROFILE_TMPL_CONTENT = {
  'title'       	: 'Profile Management',
  'template'    	: 'actions.html',
  'actions'     	: ACTIONS,
  'modify': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][0]['label'],
    'desc'     		: ACTIONS[0]['actions'][0]['desc'],
    'submit'   		: 'Modify',
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Profile modified.',
    },
  },
  'adduser': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][1]['label'],
    'desc'     		: ACTIONS[0]['actions'][1]['desc'],
    'submit'   		: 'Add',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'User added.',
    },
  },
  'tiltuser': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][2]['label'],
    'desc'     		: ACTIONS[0]['actions'][2]['desc'],
    'submit'   		: 'Delete',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'User deleted.',
    },
  },
  'invoice': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][3]['label'],
    'desc'     		: ACTIONS[0]['actions'][3]['desc'],
    'submit'   		: 'View',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'Invoice.',
    },
  },
}
