# Application settings for attendance app
# coding=utf-8

ACTIONS = {
  'invite': (
    {
      'label' 		: u'Inviter un(des) ami(s), conférencier(s) ou would-be(s).',
      'icon'     	: 'plus',
      'url'           	: '/meetings/invite/',
    },
  ),
}
 
ATTENDANCE_TMPL_CONTENT = {
  'template'	: 'done.html',
  'too_late' 	: u'Désolé il est <strong>trop tard</strong> pour s\'inscrire/désister!',
  'actions'  	: ACTIONS['invite'],
  'yes'  	: u'%(name)s, par la présente ta <strong>participation</strong> est <strong>confirmé(e)</strong>!',
  'no'  	: u'%(name)s, merci de nous avoir notifier ton désistement, tu sera <strong>excusé(e)</strong>!',
  'details'  	: u'''<p>Pour rappel:
<ul>
<strong>Lieu  : %(location)s</strong><br/>
%(address)s<br/>
<em>Date  : %(when)s</em><br/>
Heure : %(time)s<br/>
</ul></p>
''',
  'event': {
    'title'	: u'Participation à l\'événement "%(event)s"',
    'email' : {
      'yes'	: u'''
Par la présente ta participation à l\'événement "%(event)s" est confirmé(e)!''',
      'no'  	: u'''
Merci de nous avoir notifié ton désistement pour l\'événement "%(event)s". 

Tu sera excusé(e).''',
    },
  },
  'meeting': {
    'title'      : u'Participation à la %(meeting)s',
    'email' : {
      'yes'	: u'''
Par la présente ta participation à la %(meeting)s est confirmé(e)!''',
      'no'  	: u'''
Merci de nous avoir notifié ton désistement pour la %(meeting)s. 

Tu sera excusé(e).''',
    },
  },
}

