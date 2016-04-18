# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

config = app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"
login_manager.login_message = "Увійдіть, щоб отримати доступ до цієї сторінки"
from werkzeug.serving import make_ssl_devcert
make_ssl_devcert('./ssl', host='localhost')

import views, models
