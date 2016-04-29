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
      'email': {
	'template'	: 'meeting_invitation.txt',
	'subject'	: u'[CLUSIL] %(title)s',
      },
    },
  },
  'send': {
    'template'		: 'form.html',
    'title'         	: u'(R)Envoyer Invitations',
    'desc'          	: u'Envoie ou renvoie les invitations pour la réunion statutaire choisie, par e-mail.',
    'submit'   		: u'Envoyer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations pour la : %s envoyées',
      'message'     	: u'Destinataires : ',
      'email': {
	'template'	: 'meeting_invitation.txt',
	'subject'	: u'[51 aperta] %(title)s',
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
      'title'   	: u'Modify %(meeting)s',
      'next'    	: 'next',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : u'Meeting [%s] has been modified!',
    },
  },
  'details': {
    'template'  	: 'done.html',
    'title'     	: u'Details of meeting: %(meeting)s (%(date)s)',
    'overview' : {
      'template'	: 'overview_meeting.html',
      'modify'		: u'Modify',
      'date'		: u'Date and time',
      'attach'		: u'Supplementary information',
      'location'	: u'Location (venue)',
      'report'		: u'Minutes',
      'attendance'	: u'Present',
      'excused'		: u'Excused',
    },
  },
  'report': {
    'template'		: 'form.html',
    'title'         	: u'Minutes of meeting: {meeting}',
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
}

