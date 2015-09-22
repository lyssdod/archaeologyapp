import os
import json 

WTF_CSFR_ENABLED = True
SECRET_KEY = "2asg84DF*#sdfETPQ21084ci"

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

CLIENT_ID = json.loads(
            open('client_secrets.json', 'r').read())['web']['client_id']

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1612012042349839',
        'secret': '9aca22d8254af6d13b9b0264945f62cb'
        },
    }
MAX_SEARCH_RESULTS = 50


