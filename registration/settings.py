# Application settings for registration app
# coding=utf-8


ACTIONS = (
  {
    'label'	: 'Individual',
    'price'	: '1 user: 100',
    'icon'    	: 'user',
    'grade'    	: 'info',
    'url'     	: '/reg/individual/',
  },
  {
    'label'	: 'Organisation',
    'price'	: 'per group of 6 users: 400',
    'icon'    	: 'building',
    'grade'    	: 'success',
    'url'     	: '/reg/organisation/',
  },
  {
    'label'	: 'Student',
    'price'	: '1 user: 25',
    'icon'    	: 'user-graduate',
    'grade'    	: 'warning',
    'url'     	: '/reg/student/',
  },
)
 

REGISTRATION_TMPL_CONTENT = {
  'home' : {
    'template'		: 'action-list.html',
    'title'		: 'Registration as <i>CLUSIL member</i>',
    'desc'  		: 'CLUSIL memberships come in 3 flavours:', 
    'actions'		: ACTIONS,
  },
  'register' : {
    'title'		: 'Register as <i>{type}</i>',
    'first'		: 'first',
    'prev'		: 'previous',
    'overview' : {
      'title'		: 'Overview',
    },
    'address' : {
      'title'   	: 'Address',
      'desc'   		: '''Please provide your detailed address.''',
      'next'    	: 'next',
    },
    'head' : {
      'title'   	: 'Head of List',
      'desc'   		: '''The head-of-list is the main point of contact and does have full rights to manage the membership (create/delete users, change membership profile, etc.).''',
      'next'          	: 'next',
    },
    'delegate' : {
      'title'           : 'Delegate',
      'desc'   		: '''The delegate is the head-of-list's alternate for all it's roles: point of contact and membership management.''',
      'next'            : 'next',
    },
    'more' : {
      'title'           : 'All Users for membership',
      'desc'   		: '''Provide the Names and Emails of all Users of your membership.''',
      'next'            : 'next',
    },
    'student_proof' : {
      'title'           : 'Student proof',
      'desc'   		: '''Do be accepted for the student membership discount, a proof is needed. Please upload scan/copy of your student card.''',
      'next'            : 'next',
    },
    'group' : {
      'title'           : 'Your Involvement',
      'desc'   		: '''CLUSIL is an association of active involvement, please choose one or more working groups (topics) <b>you</b> want to contribute to.''',
      'next'            : 'next',
    },
    'done' : {
      'template'        : 'reg_done.html',
      'title'           : 'Registration successful!',
      'error_template' 	: 'done.html',
      'email_template' 	: 'registration.txt',
    },
  },
  'validate' : {
    'template'		: 'done.html',
    'title'		: 'Membership validation',
    'done_message' 	: u'''Dear {name},
<br/><br/>
Welcome to <strong>CLUSIL</strong>!
<br/><br/>
Your membership is now validated.
<br/>
<em>[MEMBER_ID: {member_id}]</em>
<br/><br/>
The membership invoice will reach you in a seperate email, please pay your fee in a timely manner.
<br/><br/>
For any further communication please use the above MEMBER_ID for best service experience.
<br/><br/>
Looking forward to meet you at one of our next events or working groups.
''',  
    'error_message' 	: '<strong>ERROR!</strong> Validation code not known or already used.',
    'email' : {
      'template' 	: 'validation.txt',
      'org_msg'		: u'''
As \'head-of-list\' for your organisation ({orga}), you\'re our prefered contact person and will get regular information and/or invitations to our events. You (and your delegate, if identified) have the privilege to manage the Member account and registered users.''',
       'users_msg'	: u'''
Find herebelow the list of all registered Users for this membership:
{users}
''',
    },
  },
  'board_reg' : {
    'title'		: 'Add a Member',
  },
}
