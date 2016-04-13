from myapp import db, app, login_manager

import datetime
from flask.ext.login import UserMixin
import flask.ext.whooshalchemy as whooshalchemy

@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

#lm = LoginManager(app)

#class User(UserMixin, db.Model):
#    __tablename__ = 'users'
#    id = db.Column(db.Integer, primary_key=True)
#    social_id = db.Column(db.String(64), nullable=False, unique=True)
#    nickname = db.Column(db.String(64), nullable=False)
#    email = db.Column(db.String(64), nullable=True)

#@lm.user_loader
#def load_user(id):
#    return User.query.get(int(id))
#
class Site(db.Model):
    __tablename__ = 'site'
    __searchable__= ['name', 'toponim']

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(250))
    toponim = db.Column(db.String(250))
    type_of_site= db.Column(db.String(250), nullable=False)
    oblast = db.Column(db.String(250), nullable=False)
    rajon = db.Column(db.String(250), nullable=False)
    punkt = db.Column(db.String(250), nullable=False)
    pryvjazka = db.Column(db.String(250), nullable=False)
    krajina = db.Column(db.String(250), nullable=False)
##    kultnal = db.Column(db.String(250), nullable=False)
    skiph = db.Column(db.String(250), nullable=True)
    juhn = db.Column(db.String(250), nullable=True)
    pjuhn = db.Column(db.String(250), nullable=True)
    verok = db.Column(db.String(250), nullable=True)
    dvosh = db.Column(db.String(250), nullable=True)
    drz = db.Column(db.String(250), nullable=True)
#    #
    localgr = db.Column(db.String(250), nullable=False)
    chron = db.Column(db.String(250), nullable=False)
    nadijnist = db.Column(db.String(250), nullable=False)
    rozkop = db.Column(db.String(1000), nullable=True)
    dospl = db.Column(db.Integer, nullable=False)
    zvit = db.Column(db.String(1000), nullable=False)
    publicacii = db.Column(db.String(1500), nullable=False)
    kartograph = db.Column(db.String(20), nullable=True)
    latd = db.Column(db.Float, nullable=False)
    longt = db.Column(db.Float, nullable=False)
    tochkart = db.Column(db.String(20), nullable=False)
    basejn = db.Column(db.String(50), nullable=False)
    toppotype = db.Column(db.String(30), nullable=False)
    geomorform = db.Column(db.String(250), nullable=False)
    vysotnadrm = db.Column(db.Integer, nullable=False)
    ploshch = db.Column(db.Integer, nullable=False)
    dovz = db.Column(db.Integer, nullable=False)
    shyr = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(50), nullable=True)
    plans = db.Column(db.String(50), nullable=True)
    znahidky = db.Column(db.String(50), nullable=True)
    kistka = db.Column(db.String(50), nullable=True)
    zalizo = db.Column(db.String(50), nullable=True)
    kamin = db.Column(db.String(50), nullable=True)
    glyna = db.Column(db.String(50), nullable=True)
    prymitky = db.Column(db.String(3000))

    def __init__(self, name, toponim, 
            type_of_site, oblast, rajon, krajina, punkt, pryvjazka, skiph, juhn, pjuhn, verok, dvosh, drz, localgr, chron, nadijnist, rozkop, dospl, zvit, publicacii, kartograph, latd, longt, tochkart, basejn, toppotype, geomorform, vysotnadrm, ploshch, dovz, shyr, foto, plans, znahidky, kistka, zalizo, kamin, glyna, prymitky
            ): 
        self.name = name
        self.toponim = toponim
        self.type_of_site = type_of_site
        self.oblast = oblast
        self.rajon = rajon
        self.krajina = krajina
        self.punkt = punkt
        self.pryvjazka = pryvjazka
        self.skiph = skiph
        self.juhn = juhn
        self.pjuhn = pjuhn
        self.verok = verok
        self.dvosh = dvosh
        self.drz = drz
        self.localgr = localgr
        self.chron = chron
        self.nadijnist = nadijnist
        self.rozkop = rozkop
        self.dospl = dospl
        self.zvit = zvit
        self.publicacii = publicacii
        self.kartograph = kartograph
        self.latd = latd
        self.longt = longt
        self.tochkart = tochkart
        self.basejn = basejn
        self.toppotype = toppotype
        self.geomorform = geomorform
        self.vysotnadrm = vysotnadrm
        self.ploshch = ploshch
        self.dovz = dovz
        self.shyr= shyr
        self.foto = foto
        self.plans = plans
        self.znahidky = znahidky
        self.kistka = kistka
        self.zalizo = zalizo
        self.kamin = kamin
        self.glyna = glyna
        self.prymitky = prymitky

    def __repr__(self):
        return '<Site %r>' % self.name

whooshalchemy.whoosh_index(app, Site)

