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
#class Auth:
#    CLIENT_ID = ('945184504031-t8sa0ha767vdjd7l3d45c6q638hdoqes.apps.googleusercontent.com')
#    CLIENT_SECRET = 'DTHJDsfqm_J-cy8lf1zP18t0'
#    REDIRECT_URI = 'https://localhost:5000/gCallback'
#    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
#    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
#    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
#
#class Config:
#    APP_NAME = "archaeology app"
#    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
#class DevConfig(Config):
#    DEBUG = True
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "site.db")
#config = {
#        "dev": DevConfig,
#        "default": DevConfig
#        }

#SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

#CLIENT_ID = json.loads(
#            open('client_secrets.json', 'r').read())['web']['client_id']

#OAUTH_CREDENTIALS = {
#    'facebook': {
#        'id': '1612012042349839',
#        'secret': '9aca22d8254af6d13b9b0264945f62cb'
#        },
#    }
#MAX_SEARCH_RESULTS = 50
#
#
