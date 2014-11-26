# Application settings for dav app
# coding=utf-8

DAV_TMPL_CONTENT = {
  'upload': {
    'template'	: 'upload.html',
    'title'     : 'Upload file',
    'desc'     	: '',
    'submit'   	: 'Upload',
    'done': {
      'template'	: 'done.html',
      'title'     	: 'File Upload successfully',
      'message'     	: 'File: [%(file)s] sucessfully uploaded to [%(folder)s]',
    },
  },
}

