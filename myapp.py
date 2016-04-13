from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

from werkzeug.serving import make_ssl_devcert
make_ssl_devcert('./ssl', host='localhost')

import views, models
