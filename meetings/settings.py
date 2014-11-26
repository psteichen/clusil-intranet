# Application settings for meetngs app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choose actions on <strong>meetings</strong>:',
    'has_perms'         : 'clusil.SECR',
    'actions' : (
      {
        'label'         : 'Add Meeting',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Add a new meeting',
        'url'           : '/meetings/add/',
    	'has_perms'     : 'clusil.SECR',
      },
      {
        'label'         : 'Modify Meeting',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Modify a meeting',
        'url'           : '/meetings/modify/',
    	'has_perms'     : 'clusil.SECR',
      },
      {
        'label'         : 'List Meetings',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'List all meetings',
        'url'           : '/meetings/list_all/',
    	'has_perms'     : 'clusil.SECR',
      },
    ),
  },
  {
    'heading'           : 'Choose actions on <strong>locations</strong>:',
    'has_perms'         : 'clusil.SECR',
    'actions' : (
      { 
        'label'         : 'Add Location', 
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Add a Meeting Location.', 
        'url'           : '/meetings/location/add/', 
    	'has_perms'     : 'clusil.SECR',
      },
      {
        'label'         : 'Modify Location',
        'glyphicon'     : 'glyphicon-calendar',
        'desc'          : 'Modify a location',
        'url'           : '/meetings/location/modify/',
    	'has_perms'     : 'clusil.SECR',
      },
    ),
  },
)

MEETINGS_TMPL_CONTENT = {
  'title'       : 'Meeting Management',
  'template'    : 'actions.html',
  'actions'     : ACTIONS,
  'add': {
    'template'	: 'form.html',
    'title'     : ACTIONS[0]['actions'][0]['desc'],
    'desc'     	: 'Create Meeting & Send Invitations',
    'submit'   	: 'GO',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'New Meeting added',
      'message'     	: 'and invitations sent to: ',
      'email': {
	'template'	: 'meeting_invitation.txt',
	'subject'	: '[51 aperta] %(title)s',
      },
    },
  },
  'attendance': {
    'template'	: 'done.html',
    'title'     : u'Participation à la %(meeting)s',
    'yes'  	: u'%(name)s, par la présente ta participation est confirmé(e)!',
    'no'  	: u'%(name)s, merci de nous avoir notifier ton désistement, tu sera excusé(e)!',
  },
  'list_all': {
    'template'  : 'list.html',
    'title'     : 'Liste des réunions',
    'desc'     	: ACTIONS[0]['actions'][2]['desc'],
  },
  'list': {
    'template'  : 'done.html',
    'title'     : u'Détail de la %(num)s. réunion statutaire',
    'overview' : {
      'template'	: 'overview_meeting.html',
      'date'		: u'Date et heure',
      'location'	: u'Lieu',
      'attendance'	: u'Présent(s)',
      'excused'		: u'Excusé(s)',
    },
  },
  'modify' : {
    'title'     : ACTIONS[0]['actions'][1]['label'],
    'first'	: 'first',
    'prev'	: 'back',
    'list' : {
      'title'   : 'Choose Meeting to modify',
      'next'    : 'next',
    },
    'meeting' : {
      'title'   : 'Modify Meeting',
      'next'    : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : 'Meeting [%s] modified!',
    },
  },
  'location' : {
    'add': {
      'template'	: 'form.html',
      'title'     	: ACTIONS[1]['actions'][0]['label'],
      'desc'     	: ACTIONS[1]['actions'][0]['desc'],
      'submit'   	: 'Create Meeting Location',
      'done': {
        'template'	: 'done.html',
        'title'     	: 'New Meeting Location added',
        'message'     	: 'Details here: ',
      },
    },
    'modify' : {
      'title'     	: ACTIONS[1]['actions'][1]['label'],
      'first'           : 'first',
      'prev'            : 'back',
      'list' : {
        'title'         : 'Choose Location to modify',
        'next'          : 'next',
      },
      'location' : {
        'title'         : 'Modify Location',
        'next'          : 'submit',
      },
      'done' : {
        'template'      : 'done.html',
        'title'         : 'Location [%s] modified!',
      },
    },
  },
}

