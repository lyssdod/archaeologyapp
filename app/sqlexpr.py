from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#enable_search = True
import flask.ext.whooshalchemy as whooshalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thetest.db'
db = SQLAlchemy(app)
#app.config['WHOOSH_BASE']='here/base'

class User(db.Model):
    __tablename__ = 'user'
    __searchable__ = ['username', 'email']
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

#db.create_all()
#from sqlexpr import User
#admin = User(username = 'admin', email = 'admin@example.com')
#guest = User('guest', 'guest@example.com')

#db.session.add(admin)
#db.session.add(guest)
#db.session.commit()
#if enable_search:
whooshalchemy.whoosh_index(app, User)

@app.route('/')
def welcome():
#    user= User.query.filter_by(username='theadmin').first() #User.query.all()
    results = User.query.whoosh_search('day').one()
    return  '%s' %results.username #'%s' % user.username

if __name__ == '__main__':
    app.debug=True
    app.run(host ='0.0.0.0', port=5000)
