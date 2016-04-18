import os
#import json 
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSFR_ENABLED = True
SECRET_KEY = "2asg84DF*#sdfETPQ21084ci"

GOOGLE_LOGIN_CLIENT_ID = "945184504031-t8sa0ha767vdjd7l3d45c6q638hdoqes.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "DTHJDsfqm_J-cy8lf1zP18t0"

OAUTH_CREDENTIALS={
    'google': {
        'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
                                                }
                }

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#MAX_SEARCH_RESULTS = 50
#
#
