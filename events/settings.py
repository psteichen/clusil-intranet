# Application settings for events app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'           : u'New event',
      'icon'            : 'plus',
      'grade'           : 'success',
      'url'             : '/events/add/',
      'has_perms'       : 'cms.SECR',
    },
  ),
}

EVENTS_TMPL_CONTENT = {
  'title'       	: u'Events',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'New event',
    'desc'     		: u'This creates a new event and prepares the invitations to be send.',
    'submit'   		: u'add',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'New event created.',
      'message'     	: '''
<pre>
Invitation message: 
--------------------------------------
%(email)s
--------------------------------------

Recipients : 
%(list)s
</pre>
''',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: u'%(title)s',
      },
    },
  },
  'send': {
    'template'		: 'form.html',
    'title'     	: u'(R)Send invitations',
    'desc'              : u'Envoie ou renvoie les invitations pour l\'évènement choisie, par e-mail.',
    'submit'            : u'Envoyer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations pour la : %s envoyées',
      'message'         : u'Destinataires : ',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: u'%(title)s',
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
      'invitation'      : u'Invitation',
      'attachement'     : u'Attachement',
    },
  },
}
