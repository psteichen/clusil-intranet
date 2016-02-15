# Application settings for profile app
# coding=utf-8

ACTIONS = (
  {
    'label'	: 'Change Profile',
    'icon'	: 'pencil',
    'grade'	: 'warning',
    'url'    	: '/profile/modify/',
  },
  {
    'label'	: 'Affiliate User',
    'icon'	: 'th-list',
    'grade'	: 'info',
    'url'     : '/profile/affiluser/',
  },
  {
    'label'	: 'Add User',
    'icon'	: 'plus',
    'grade'	: 'success',
    'url'     : '/profile/adduser/',
  },
  {
    'label'	: 'Delete User',
    'icon'	: 'minus',
    'grade'	: 'danger',
    'url'    	: '/profile/rmuser/',
  },
)

PROFILE_TMPL_CONTENT = {
  'profile': {
    'template'          : 'overview.html',
    'actions'           : ACTIONS,
    'title'             : u'Member profile for <i>%(member)s</i>',
    'overview' : {
      'template'        : 'overview_member.html',
      'managers'       	: u'Managers',
      'firstname'       : u'Firstname',
      'name'            : u'Name',
      'login'        	: u'Login',
      'email'           : u'E-mail',
      'role'            : u'Role',
      'affil'          	: u'Affiliation',
    },
  },
  'modify': {
    'template'		: 'form.html',
    'title'     	: 'Modify Profile',
    'desc'	     	: 'Modify CLUSIL Membership profile',
    'submit'   		: 'Modify',
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Profile modified.',
    },
  },
  'adduser': {
    'template'		: 'form.html',
    'title'     	: 'Add User',
    'desc' 	    	: 'Add a new User to the Membership',
    'submit'   		: 'Add',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'User added.',
    },
  },
  'affiluser': {
    'template'		: 'form.html',
    'title'     	: 'Affiliate User',
    'desc'     		: 'Affiliate a User to a Working Group or Tool',
    'submit'   		: 'Affiliate',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'User affiliated.',
    },
  },
  'rmuser': {
    'template'		: 'form.html',
    'title'     	: 'Remove User',
    'desc'     		: 'Remove a User from the CLUSIL Membership',
    'submit'   		: 'Remove',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'User removed.',
    },
  },
  'invoice': {
    'template'		: 'form.html',
    'title'     	: 'View Invoices',
    'desc'     		: 'View Invoices and payment status of the CLUSIL Membership',
    'submit'   		: 'View',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'Invoice.',
    },
  },
}
