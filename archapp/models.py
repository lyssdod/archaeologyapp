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
    type_of_site= db.Column(db.String(250), nullable=False)
    oblast = db.Column(db.String(250), nullable=False)
    rajon = db.Column(db.String(250), nullable=False)
    punkt = db.Column(db.String(250), nullable=False)
    pryvjazka = db.Column(db.String(250), nullable=False)
    kultnal = db.Column(db.String(250), nullable=False)
    localgr = db.Column(db.String(250), nullable=False)
    chron = db.Column(db.String(250), nullable=False)
    nadijnist = db.Column(db.String(250), nullable=False)
    rozkop = db.Column(db.String(1000), nullable=False)
    zvit = db.Column(db.String(1000), nullable=False)
    publicacii = db.Column(db.String(1500), nullable=False)
    kartograph = db.Column(db.String(20), nullable=False)
    coord = db.Column(db.String(50), nullable=False)
    tochkart = db.Column(db.String(20), nullable=False)
    basejn = db.Column(db.String(50), nullable=False)
    toppotype = db.Column(db.String(30), nullable=False)
    geomorform = db.Column(db.String(250), nullable=False)
    vysotnadrm = db.Column(db.Integer, nullable=False)
    ploshch = db.Column(db.Integer, nullable=False)
    dovz = db.Column(db.Integer, nullable=False)
    shyr = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(50))
    plans = db.Column(db.String(50), nullable=False)
    znahidky = db.Column(db.String(50), nullable=False)
    kistka = db.Column(db.String(50), nullable=False)
    zalizo = db.Column(db.String(50), nullable=False)
    kamin = db.Column(db.String(50), nullable=False)
    glyna = db.Column(db.String(50), nullable=False)
    prymitky = db.Column(db.String(3000))

    def __init__(self, name, toponim, type_of_site, oblast, rajon, punkt, pryvjazka, kultnal, localgr, chron, nadijnist, rozkop, zvit, publicacii, kartograph, coord, tochkart, basejn, toppotype, geomorform, vysotnadrm, ploshch, dovz, shyr, foto, plans, znahidky, kistka, zalizo, kamin, glyna, prymitky): 
        self.name = name
        self.toponim = toponim
        self.type_of_site = type_of_site
        self.oblast = oblast
        self.rajon = rajon
        self.punkt = punkt
        self.pryvjazka = pryvjazka
        self.kultnal = kultnal
        self.localgr = localgr
        self.chron = chron
        self.nadijnist = nadijnist
        self.rozkop = rozkop
        self.zvit = zvit
        self.publicacii = publicacii
        self.kartograph = kartograph
        self.coord = coord
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

