# Application settings for registration app
# coding=utf-8


REGISTRATION_TMPL_CONTENT = {
  'register' : {
    'title'		: 'Registration',
    'first'		: 'first',
    'prev'		: 'previous',
    'overview' : {
      'title'		: 'Overview',
    },
    'type' : {
      'title'   	: 'Membership',
      'desc'   		: '''CLUSIL memberships come in 3 variants: 
<ul>
 <li>Individual (1 user:  100€) ;</li>
 <li>Organisation (per group 6 users: 400€) ;</li>
 <li>Student (1 user: 25€ [student proof required])</li>
</ul>''',  
      'next'    	: 'next',
    },
    'address' : {
      'title'   	: 'Address',
      'desc'   		: '''Please provide your detailed address.''',
      'next'    	: 'next',
    },
    'head' : {
      'title'   	: 'Head of List',
      'desc'   		: '''The head-of-list is the main point of contact and does have full rights to manage the membership (create/delete users, change membership profile, etc.).''',
      'alttitle'   	: 'User',
      'altdesc' 	: 'Create a user for the CLUSIL Member Intranet Platform.',
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
      'title'           : 'Involvement',
      'desc'   		: '''CLUSIL is an association of active involvement, please choose one or more working groups (topics) you want to contribute to.''',
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
    'done_message' 	: '''Dear {name},
<br/><br/>
Welcome to <strong>CLUSIL</strong>!
<br/><br/>
Your membership is now validated.
<br/>
<em>[MEMBER_ID: {member_id}]</em>
<br/><br/>
For any further communication please use the above MEMBER_ID for best service experience.
<br/><br/>
Looking forward to meet you at one of our next events or working groups.
''',  
    'error_message' 	: '<strong>ERROR!</strong> Validation code not known or already used.',
    'email' : {
      'template' 	: 'validation.txt',
      'org_msg'		: u'''
As \'head-of-list\' for your organisation ({orga}), you have the privilege to manage the Member account and add further users (up to 6 in total). 
You\'re also our prefered contact person and will get regular information and/or invitations to our events.''',
    },
  },
}
