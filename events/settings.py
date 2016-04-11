# Application settings for events app
# coding=utf-8

ACTIONS = {
  'main': (
    {
      'label'           : u'Ajouter un évènement',
      'icon'            : 'plus',
      'url'             : '/events/add/',
      'has_perms'       : 'cms.COMM',
    },
    {
      'label'           : u'Gestion des Lieux de Rencontre',
      'icon'            : 'home',
      'url'             : '/locations/',
      'has_perms'       : 'cms.COMM',
    },
  ),
}

EVENTS_TMPL_CONTENT = {
  'title'       	: u'Évènements',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['main'],
  'add': {
    'template'		: 'form.html',
    'title'     	: u'Créer un évènement',
    'desc'     		: u'Ceci créé un évènement et prépare les invitations à envoyer.',
    'submit'   		: u'Ajouter',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Nouvel évènement créé.',
      'message'     	: '''
<pre>
Message d'invitation : 
--------------------------------------
%(email)s
--------------------------------------

Destinataires : 
%(list)s
</pre>
''',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: u'[51 aperta] %(title)s',
      },
    },
  },
  'send': {
    'template'		: 'form.html',
    'title'     	: u'(R)Envoyer Invitations',
    'desc'              : u'Envoie ou renvoie les invitations pour l\'évènement choisie, par e-mail.',
    'submit'            : u'Envoyer',
    'done': {
      'template'	: 'done.html',
      'title'     	: u'Invitations pour la : %s envoyées',
      'message'         : u'Destinataires : ',
      'email': {
	'template'	: 'event_invitation.txt',
	'subject'	: u'[51 aperta] %(title)s',
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
    'meeting' : {
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
    'title'             : u'Détail de l\'évènement %(event)s',
    'overview' : {
      'template'        : 'overview_event.html',
      'modify'          : u'Modifier',
      'date'            : u'Date et heure',
      'location'        : u'Lieu de rencontre',
      'attendance'      : u'Présent(s)',
      'excused'         : u'Excusé(s)',
    },
  },
}
