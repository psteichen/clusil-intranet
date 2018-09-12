# Application settings for profile app
# coding=utf-8

ACTIONS = (
  {
    'label'	: 'Change Profile',
    'icon'	: 'pencil',
    'grade'	: 'warning',
    'url'    	: '/profile/modify/',
    'has_perms'	: 'HEAD-OF-LIST',
  },
  {
    'label'	: 'Invoices',
    'icon'	: 'euro',
    'grade'	: 'info',
    'url'    	: '/profile/invoice/',
    'has_perms'	: 'HEAD-OF-LIST',
  },
)
ACTIONS_ORG = (
  {
    'label'	: 'Add User',
    'icon'	: 'plus',
    'grade'	: 'success',
    'url'	: '/profile/adduser/',
    'has_perms'	: 'HEAD-OF-LIST',
  },
)
INV_ACTIONS = (
  {
    'label'	: 'Generate Invoice',
    'icon'	: 'euro',
    'grade'	: 'warning',
    'url'	: '/profile/invoice/new/',
    'has_perms'	: 'HEAD-OF-LIST',
  },
)
ADMIN_INV_ACTIONS = (
  {
    'label'	: 'Generate Invoice',
    'icon'	: 'euro',
    'grade'	: 'warning',
    'url'	: '/members/invoice/new/{}/',
  },
)


PROFILE_TMPL_CONTENT = {
  'profile': {
    'template'          : 'overview.html',
    'actions'           : ACTIONS,
    'actions_org'	: ACTIONS + ACTIONS_ORG,
    'title'             : u'Member profile <small>[%(type)s]</small> for <i>%(member)s</i>',
    'overview' : {
      'template'        : 'overview_member.html',
      'managers'       	: u'Managers',
      'firstname'       : u'Firstname',
      'name'            : u'Name',
      'login'        	: u'Login',
      'email'           : u'E-mail',
      'role'            : u'Role',
    },
    'user_overview' : {
      'template'        : 'overview_member.html',
      'managers'       	: u'Managers',
      'firstname'       : u'Firstname',
      'name'            : u'Name',
      'login'        	: u'Login',
      'email'           : u'E-mail',
      'role'            : u'Role',
    },
    'admin_overview' : {
      'template'        : 'overview_user.html',
      'firstname'       : u'Firstname',
      'name'            : u'Name',
      'login'        	: u'Login',
      'email'           : u'E-mail',
      'role'            : u'Role',
    },
  },
  'modify': {
    'template'		: 'form.html',
    'title'     	: u'Modify Profile [{id}]',
    'desc'  	   	: u'Modify/adjust your Membership Profile',
    'submit'   		: u'Modify',
    'done' : {
      'template'        : 'done.html',
      'title'           : u'Profile [{id}] modified!',
      'message'         : u'''Fields (information) modified:
{list}
''',
    },
  },
  'adduser': {
    'template'		: 'form.html',
    'title'     	: u'Add User for [{id}]',
    'desc' 	    	: u'Add a User to your membership',
    'submit'   		: u'Add',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'User [{user}] added.',
      'message'		: u'<p>{name} added successfully to your membership.</p>',
      'no_org'		: u'<p>Your membership type does only allow one(1) User.</p>',
#      'max'		: u'''<p>You already have the maximum of allowed Users for your Membership type.</p>
#<p>If you want more Users, you'll have to get the next membership level: <a href="/profile/upgrade/">Upgrade membership</a>.</p>''',
      'max'		: u'''<p>You already have the maximum of allowed Users for your Membership type.</p>
<p>If you want more Users, you'll have to get the next membership level. Contact us to <a href="mailto:membership@clusil.lu?Subject=Upgrade membership [{member_id}]">upgrade your membership</a>.</p>''',
    },
  },
#  'affiluser': {
#    'template'		: 'form.html',
#    'title'     	: u'Affiliate {name}',
#    'desc'     		: u'Procede to affiliate <i>{name}</i> to a Working Group, Ad-Hoc Group or Tool',
#    'submit'   		: u'Affiliate',
#    'done': {
#      'template'	: 'done.html',
#      'title'     	: u'{name} successfully affiliated.',
#      'message'     	: u'User <i>{name}</i> is now affiliated to the following groups: <b>{groups}</b>',
#    },
#  },
  'make_head': {
    'template'		: 'done.html',
    'title'     	: u'Changed Head of List for [{id}]',
    'message'     	: u'{head} is now your new Head of List!',
  },
  'make_delegate': {
    'template'		: 'done.html',
    'title'     	: u'Changed Delegate for [{id}]',
    'message'     	: u'{head} is now your new Delegate!',
  },
  'moduser': {
    'template'		: 'form.html',
    'title'     	: u'Modify {name}',
    'desc'     		: u'',
    'submit'   		: u'Submit',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'{name} successfully modified.',
    },
  },
  'rmuser': {
    'template'		: 'done.html',
    'title'     	: u'Delete User',
    'message'  		: u'''Are you sure to delete the following User from your Membership?
<dl class="dl-horizontal">
<dt>Name:</dt><dd>{name}</dd>
<dt>Email:</dt><dd>{email}</dd>
<dt>Login:</dt><dd>{login}</dd>
</dl>
<a href="{url}" class="btn btn-xl btn-danger"><b>Really</b> delete this User?</a>
''',
    'error': {
      'template'	: 'done.html',
      'title'     	: u'Error in deleting User.',
      'message'     	: u'You seem to have no rights to delete User, please contact your Head-of-List or Delegate.',
    },
    'done': {
      'template'	: 'done.html',
      'title'     	: u'User DELETED!',
      'message' 	: u'''The following User was deleted successfully:
<dl class="dl-horizontal">
<dt>Name:</dt><dd>{name}</dd>
<dt>Email:</dt><dd>{email}</dd>
<dt>Login:</dt><dd>{login}</dd>
</dl>
''',
    },
  },
  'invoice': {
    'template'		: 'list.html',
    'title'     	: u'Invoices',
    'desc'     		: u'View Invoices and payment status of the CLUSIL Membership',
    'actions'  		: INV_ACTIONS,
    'admin_actions'  	: ADMIN_INV_ACTIONS,
    'done': {
      'template'	: 'done.html',
      'title'     	: u'View Invoice.',
    },
  },
  'newinv': {
    'template'		: 'done.html',
    'title'     	: u'New Invoice generated for [{id}]',
    'message'     		: u'A new invoice for your CLUSIL membership fee for {year} has been generated and sent to the head-of-list. This invoice replaces and cancels all previous ones for the same year.',
  },
  'renew' : {
    'template'		: 'done.html',
    'title'		: 'Membership renewal',
    'done_message' 	: u'''Dear {name},
<br/><br/>
Thank you for your continuing support to <strong>CLUSIL</strong>!
<br/><br/>
Your membership is now renewed.
<br/>
<em>[MEMBER_ID: {member_id}]</em>
<br/><br/>
The invoice will reach you by email, please pay in a timely manner.
<br/><br/>
Looking forward meeting you again at one of our next events.
''',  
    'error_message' 	: '<strong>ERROR!</strong> Validation code not known or already used.',
    'sp': {
      'template'	: 'form.html',
      'title'     	: u'Provide Student proof for the year {year}',
      'desc'     	: u'''<p>To continue with the reduced membership fee, please provide "student proof" for the year {year}.</p>
<p>If you want to switch to the standard membership as "individual", simply submit without uploading a document.</p>''',
      'submit'   	: u'Submit',
    },
  },
}
