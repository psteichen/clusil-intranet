# Application settings for meetngs app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'         	: u'New meeting',
      'icon'     	: 'plus',
      'grade'     	: 'success',
      'url'           	: '/meetings/add/',
      'has_perms'     	: 'cms.SECR',
    },
  ),
}

MEETINGS_TMPL_CONTENT = {
  'title'       	: u'Meetings',
  'duration'       	: 2, #default duration
  'template'    	: 'list.html',
  'desc'       		: u'',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'New Meeting',
    'desc'          	: u'Create new meeting and prepare email invitations.',
    'submit'   		: u'Add',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'New Meeting created',
      'message'     	: u'''
<pre>
Invitation message: 
--------------------------------------
%(email)s
--------------------------------------

Recipients: 
%(list)s
</pre>
''',
    },
  },
  'send': {
    'template'		: 'form.html',
    'title'         	: u'(Re)send invitations',
    'desc'          	: u'(Re)Send e-mnail invitations for this meeting.',
    'submit'   		: u'Send',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations for "%s" meeting, sent',
      'message'     	: u'Recipients: ',
      'email': {
	'template'	: 'meeting_invitation.txt',
	'subject'	: u'[CLUSIL] %(title)s',
      },
    },
  },
  'modify' : {
    'title'         	: u'Modify a Meeting',
    'desc'		: u'Modify the details of a meeting.',
    'first'		: u'start',
    'prev'		: u'end',
    'list' : {
      'title'   	: u'Choose meeting to modify',
      'next'    	: 'next',
    },
    'meeting' : {
      'title'   	: u'Adjust %(meeting)s',
      'next'    	: 'next',
    },
    'invitation' : {
      'title'   	: u'Adjust invitation details',
      'next'    	: 'next',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : u'Meeting [%s] has been modified!',
    },
  },
  'details': {
    'template'  	: 'done.html',
    'title'     	: u'Details of "%(meeting)s" meeting (%(date)s)',
    'overview' : {
      'template'	: 'overview_meeting.html',
      'modify'		: u'Modify',
      'topic'		: u'Main topic of the meeting:',
      'date'		: u'Date and time',
      'message'		: u'Supplementary information:',
      'attach'		: u'Attachement',
      'location'	: u'Location (venue)',
      'report'		: u'Minutes',
      'attendance'	: u'Present',
      'excused'		: u'Excused',
    },
  },
  'report': {
    'template'		: 'form.html',
    'title'         	: u'Minutes of meeting: {}',
    'desc'          	: u'Save minutes and send it automatically to the meeting attendees (optional).',
    'submit'   		: u'Upload',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Minutes uploaded.',
      'title_send'     	: u'Minutes uploaded and sent to attendees.',
      'message'     	: u'',
      'message_send'   	: u'Reciepients : ',
      'email': {
	'template'	: 'meeting_report.txt',
	'subject'	: u'[CLUSIL] Minutes of meeting: %(title)s',
      },
    },
  },
  'delete': {
    'template'		: 'form.html',
    'title'     	: u'DELETE Meeting [%(meeting)s] ?',
    'desc'          	: u'<strong>This will permanently DELETE the meeting! Be sure that this is your intended objective!</strong>',
    'submit'   		: u'DELETE',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Meeting [%(meeting)s] DELETED',
    },
  },
}

