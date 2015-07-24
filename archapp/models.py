from myapp import db, app

from flask.ext.login import LoginManager, UserMixin
import flask.ext.whooshalchemy as whooshalchemy


lm = LoginManager(app)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class Site(db.Model):
    __tablename__ = 'site'
    __searchable__= ['name', 'toponim']

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(250))
    toponim = db.Column(db.String(250))
    def __init__(self, name, toponim): #, type_of_site, oblast, rajon): #, punkt, pryvjazka, prymitky, kultnal, localgr, chron, nadijnist, rozkop, zvit, publicacii, kartograph, coord, tochkart, basejn, toppotype, geomorform, vysotnadrm, ploshch, dovz, shyr): 
        self.name = name
        self.toponim = toponim



    def __repr__(self):
        return '<Site %r>' % self.name

whooshalchemy.whoosh_index(app, Site)

