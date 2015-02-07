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
 <li>Individual (1 user) - 100€ ;</li>
 <li>Organisation (up to 6 users) - 400€ ;</li>
 <li>Student (1 user) ; 25€ (student proof required)</li>
</ul>''',  
      'next'    	: 'next',
    },
    'address' : {
      'title'   	: 'Address',
      'desc'   		: '''Please provide your detailed address''',
      'next'    	: 'next',
    },
    'head' : {
      'title'   	: 'Head of List',
      'desc'   		: '''The head-of-list is our main point of contact and does have full rights to manage the membership (create/delete users, change membership profile, etc.)''',
      'alttitle'   	: 'User',
      'altdesc' 	: 'Create a user for the CLUSIL Member Intranet Platform.',
      'next'          	: 'next',
    },
    'delegate' : {
      'title'           : 'Delegate',
      'desc'   		: '''The delegate is the head-of-list's alternate for all it's roles: point of contact and membership management''',
      'next'            : 'next',
    },
    'student_proof' : {
      'title'           : 'Student proof',
      'desc'   		: '''Do be accepted for the student membership discount, a proof is needed. Please upload scan/copy of your student card''',
      'next'            : 'next',
    },
    'group' : {
      'title'           : 'Involvement',
      'desc'   		: '''CLUSIL is an association of active involvement, please choice your prefered working group (topic) you want to contribute to.''',
      'next'            : 'next',
    },
    'captcha' : {
      'title'           : 'Catpcha',
      'desc'   		: '',
      'next'            : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Registration successful!',
      'email_template' 	: 'registration.txt',
    },
  },
}
