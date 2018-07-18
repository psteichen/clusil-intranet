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
        'has_perms'    	: 'BOARD',
      },
      { 
        'label'        	: 'Credit Note', 
        'icon'     	: 'repeat',
        'grade'        	: 'warning', 
        'url'          	: '/accounting/credit/{id}/{year}/', 
        'has_perms'    	: 'BOARD',
      },
      { 
        'label'        	: 'New Invoice', 
        'icon'     	: 'file',
        'grade'     	: 'danger',
        'url'          	: '/accounting/invoice/{id}/{year}/', 
        'has_perms'    	: 'BOARD',
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
      'title'     	: 'Payment validated',
    },
  },
  'credit': {
    'template'		: 'done.html',
    'title'     	: 'Credit note generated for',
    'message'     	: '''<ul class="list-group">
	<li class="list-group-item">Member: {member}</li>
	<li class="list-group-item">Year: {year}</li>
	<li class="list-group-item">Head-of-list: {head}</li>
</ul>''',
  },
  'invoice': {
    'template'		: 'done.html',
    'title'     	: 'New Invoice generated for',
    'message'     	: u'''<ul class="list-group">
	<li class="list-group-item">Member: {member}</li>
	<li class="list-group-item">Year: {year}</li>
	<li class="list-group-item">Head-of-list: {head}</li>
</ul>''',
  },
}
