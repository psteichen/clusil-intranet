# Application settings for accounting app
# coding=utf-8

ACTIONS = {
  'list' : {
    'main' : (
    ),
    'table' : (
      { 
        'label'        	: 'Validate payment', 
        'icon'     	: 'ok',
        'grade'        	: 'success', 
        'url'          	: '/accounting/payment/{id}/{year}/', 
        'has_perms'    	: 'cms.BOARD',
      },
      { 
        'label'        	: 'Credit Note', 
        'icon'     	: 'repeat',
        'grade'        	: 'warning', 
        'url'          	: '/accounting/credit/{id}/{year}/', 
        'has_perms'    	: 'cms.BOARD',
      },
      { 
        'label'        	: 'New Invoice', 
        'icon'     	: 'file',
        'grade'     	: 'danger',
        'url'          	: '/accounting/invoice/{id}/{year}/', 
        'has_perms'    	: 'cms.BOARD',
      },
    ),
  },
}

ACCOUNTING_TMPL_CONTENT = {
  'title'       	: 'Accounting',
  'template'    	: 'list.html',
  'actions'     	: ACTIONS['list'],
  'invoice': {
    'template'		: 'form.html',
    'title'     	: 'Produce Invoice',
    'desc'     		: '',
    'submit'   		: 'Generate',
  },
  'payment': {
    'template'		: 'form.html',
    'title'     	: 'Validate Payment',
    'desc'     		: '',
    'submit'   		: 'Validate',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'Payment validated.',
    },
  },
}
