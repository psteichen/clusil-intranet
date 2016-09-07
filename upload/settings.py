

UPLOAD_TMPL_CONTENT = {
  'template'		: 'form.html',
  'submit'   		: u'Submit',
  'done': {
    'template'	: 'done.html',
  },
  'gen': {
    'title'    		: u'Upload file',
    'desc'		: u'',
    'email': {
      'template'   	: u'upload.txt',
      'subject'     	: u'Generic submission.',
      'to'   		: u'board@clusil.lu',
      'message'   	: u'Please find below a generic submission.',
    },
    'done': {
      'title'     	: u'Thank you',
      'message'   	: u'File successfully uploaded.',
    },
  },
  'survey-ism': {
    'title'    		: u'Upload ISM benchmark questionnaire',
    'desc'		: u'''
<p>Privacy and anonymity of the respondent is the critical success factor of such survey and CLUSIL considers privacy and anonymity of the respondents as its highest priority.</p>
<p>The questionnaire will be anonymously uploaded within this restricted area of the CLUSIL.</p>
<p>Once uploaded, the filled out form will be anonymously posted to a specific mailing-list of the CLUSIL for analysis.</p>
<p>Anonymity is preserved at all circumstances.</p>
<p>No logs of the uploading activity will be kept.</p>
''',
    'email': {
      'template'   	: u'upload.txt',
      'subject'     	: u'Submission for the ISM benchmark.',
      'to'   		: u'cedric.mauny@clusil.lu',
      'message'   	: u'Please find below a submission for the ISM benchmark.',
    },
    'done': {
      'title'     	: u'Thank you',
      'message'   	: u'For your submission for the ISM benchmark.',
    },
  },
  'import': {
    'members': {
      'template'          : 'form.html',
      'title'             : u'Import Members',
      'desc'              : u"Only, specially crafted CSV data files are accepted!",
      'submit'            : u'Import',
      'done': {
        'template'        : 'done.html',
        'title'           : u'{nb} Member(s) imported.',
        'message'         : u'Details: ',
      }, 
    },
  },
}

