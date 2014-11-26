# Application settings for accounting app
# coding=utf-8

ACTIONS = (
  {
    'heading'           : 'Choose accounting actions:',
    'has_perms'         : 'clusil.BOARD',
    'actions'   : (
      { 
        'label'         : 'Produce Invoice', 
        'glyphicon'     : 'glyphicon-euro',
        'desc'          : 'Produce or re-generate an Invoice', 
        'url'           : '/accounting/invoice/', 
	'has_perms'     : 'clusil.BOARD',
      },
      { 
        'label'         : 'Validate payment', 
        'glyphicon'     : 'glyphicon-th-large',
        'desc'          : 'Validate a payment', 
        'url'           : '/accounting/payment/', 
	'has_perms'     : 'clusil.BOARD',
      },
    ),
  },
)

ACCOUNTING_TMPL_CONTENT = {
  'title'       	: 'Accounting',
  'template'    	: 'actions.html',
  'actions'     	: ACTIONS,
  'invoice': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][0]['label'],
    'desc'     		: ACTIONS[0]['actions'][0]['desc'],
    'submit'   		: 'Generate',
  },
  'payment': {
    'template'		: 'form.html',
    'title'     	: ACTIONS[0]['actions'][1]['label'],
    'desc'     		: ACTIONS[0]['actions'][1]['desc'],
    'submit'   		: 'Validate',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'Invoices validated.',
    },
  },
}
