# Application settings for attendance app
# coding=utf-8

ACTIONS = {
  'invite': (
    {
      'label' 		: u'Invite (a) collegue(s).',
      'grade'     	: 'info',
      'icon'     	: 'plus',
      'url'           	: '/meetings/invite/',
    },
  ),
}
 
ATTENDANCE_TMPL_CONTENT = {
  'template'	: 'done.html',
  'too_late' 	: u'Sorry, it is <strong>too late</strong> to confirm/cancel your participation!',
#  'actions'  	: ACTIONS['invite'],
  'actions'  	: None,
  'yes'  	: u'%(name)s, herewith your <strong>participation</strong> is <strong>confirmed</strong>!',
  'no'  	: u'%(name)s, thank you for notifying us your cancellation, you will be <strong>excused</strong>!',
  'details'  	: u'''<p>For your reminder:
<ul>
<strong>Location: %(location)s</strong><br/>
<em>Date: %(when)s</em><br/>
Time: %(time)s<br/>
</ul></p>
''',
  'event': {
    'title'	: u'Your participation to the following event: "%(event)s"',
    'email' : {
      'yes'	: u'''
Herewith your participation to "%(event)s" is *confirmed*!''',
      'no'  	: u'''
Thank you for notifying us your cancellation for "%(event)s".

You will be *excused*.''',
    },
  },
  'meeting': {
    'title'	: u'%(meeting)s meeting',
    'email' : {
      'yes'	: u'''
Herewith your participation to "%(meeting)s" is *confirmed*!''',
      'no'  	: u'''
Thank you for notifying us your cancellation for "%(meeting)s".

You will be *excused*.''',
    },
  },
}

