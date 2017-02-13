# Application settings for events app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'           : u'Create event',
      'icon'            : 'plus',
      'grade'           : 'success',
      'url'             : '/events/create/',
      'has_perms'       : 'cms.SECR',
    },
  ),
}

EVENTS_TMPL_CONTENT = {
  'title'       	: u'Public Events',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'email': {
    'template'	: 'event_invitation.txt',
    'subject'	: u'%(title)s',
  },
  'create' : {
    'title'             : u'Create a Public Event',
    'desc'              : u'Create a Public Event.',
    'first'             : u'first',
    'prev'              : u'prev',
    'event' : {
      'title'           : u'Event details',
      'next'            : 'next',
    },
    'distrib' : {
      'title'           : u'Choose distribution lists',
      'next'            : 'submit',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : u'[%s] created!',
    },
  },
  'send': {
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations for: "%(event)s" sent',
      'message'         : u'''
<p>Invitation message:</p>
<ul>
%(email)s
</ul>

<p>Recipients: </p>
<ul>
%(list)s
</ul>
''',
    },
  },
  'register': {
    'template'		: 'events_reg.html',
    'title'             : u'{}',
    'header'       	: u'Registration form:',
    'submit'            : u'Register',
    'teaser' : {
      'template'      	: 'teaser_event_reg.html',
      'title'           : u'Event overview:',
      'date'          	: u'Schedule',
      'location'      	: u'Venue',
      'agenda'      	: u'Agenda',
      'info'		: u'Additional information',
    },
    'email': {
      'template'	: 'event_registration.txt',
      'subject'     	: u'Thank you for registration',
    }, 
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Thank you for registering to our event: {}',
      'overview' : {
        'template'      : 'overview_event_reg.html',
        'date'          : u'Date and starting time',
        'location'      : u'Venue',
        'agenda'      	: u'Agenda',
        'info'		: u'Additional information',
        'regcode'	: u'Your Registration Code:',
      },
    },
  },
  'modify' : {
    'title'             : u'Modifier un Evènement',
    'desc'              : u'Modifier les détails et les présences d\'un évènement.',
    'first'             : u'début',
    'prev'              : u'retour',
    'list' : {
      'title'           : u'Choisir l\'évènement à modifier',
      'next'            : 'suivant',
    },
    'event' : {
      'title'           : u'Modifier l\'évènement %(event)s',
      'next'            : 'suivant',
    },
    'attendance' : {
      'title'           : u'Ajuster les présences',
      'next'            : 'soumettre',
    },
    'done' : {
      'template'        : 'done.html',
      'title'           : u'[%s] a été modifiée!',
    },
  },
  'details': {
    'template'          : 'done.html',
    'title'             : u'Detail of the event: %(event)s',
    'overview' : {
      'template'        : 'overview_event.html',
      'modify'          : u'Modify',
      'date'            : u'Date and starting time',
      'location'        : u'Venue',
      'agenda'      	: u'Agenda',
      'invitation'      : u'Invitation',
      'attachement'     : u'Attachement',
      'attendance'	: u'Registered participants',
      'registration'	: u'Registration link',
    },
  },
}
