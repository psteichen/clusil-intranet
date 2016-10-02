# Application settings for accounting app
# coding=utf-8

ACTIONS = {
  'list' : (
    { 
      'label'         	: 'Produce Invoice', 
      'icon'     	: 'euro',
      'grade'     	: 'danger',
      'url'           	: '/accounting/invoice/', 
      'has_perms'     	: 'cms.BOARD',
    },
    { 
      'label'         	: 'Validate payment', 
      'icon'     	: 'tick',
      'grade'          	: 'danger', 
      'url'           	: '/accounting/payment/', 
      'has_perms'     	: 'cms.BOARD',
    },
  ),
}

ACCOUNTING_TMPL_CONTENT = {
  'title'       	: 'Accounting',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['list'],
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
