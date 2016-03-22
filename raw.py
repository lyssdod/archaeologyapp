import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.whooshalchemy as whooshalchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Site(db.Model):
    __tablename__ = 'site'
    __searchable__= ['name', 'toponim']

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(250))
    toponim = db.Column(db.String(250))
#    type_of_site= db.Column(db.String(250), nullable=False)
#    oblast = db.Column(db.String(250), nullable=False)
#    rajon = db.Column(db.String(250), nullable=False)
#    punkt = db.Column(db.String(250), nullable=False)
#    pryvjazka = db.Column(db.String(250), nullable=False)
#    kultnal = db.Column(db.String(250), nullable=False)
#    localgr = db.Column(db.String(250), nullable=False)
#    chron = db.Column(db.String(250), nullable=False)
#    nadijnist = db.Column(db.String(250), nullable=False)
#    rozkop = db.Column(db.String(1000), nullable=False)
#    zvit = db.Column(db.String(1000), nullable=False)
#    publicacii = db.Column(db.String(1500), nullable=False)
#    kartograph = db.Column(db.String(20), nullable=False)
#    coord = db.Column(db.String(50), nullable=False)
#    tochkart = db.Column(db.String(20), nullable=False)
#    basejn = db.Column(db.String(50), nullable=False)
#    toppotype = db.Column(db.String(30), nullable=False)
#    geomorform = db.Column(db.String(250), nullable=False)
#    vysotnadrm = db.Column(db.String(250), nullable=False)
#    ploshch = db.Column(db.String(50), nullable=False)
#    dovz = db.Column(db.String(50), nullable=False)
#    shyr = db.Column(db.String(50), nullable=False)
#    prymitky = db.Column(db.String(3000))
#
    def __init__(self, name, toponim): #, type_of_site, oblast, rajon): #, punkt, pryvjazka, prymitky, kultnal, localgr, chron, nadijnist, rozkop, zvit, publicacii, kartograph, coord, tochkart, basejn, toppotype, geomorform, vysotnadrm, ploshch, dovz, shyr): 
        self.name = name
        self.toponim = toponim
#        self.type_of_site = type_of_site
#        self.oblast = oblast
#        self.rajon = rajon
#        self.punkt = punkt
#        self.prymitky = prymitky
#        self.kultnal = kultnal
#        self.localgr = localgr
#        self.chron = chron
#        self.nadijnist = nadijnist
#        self.rozkop = rozkop
#        self.zvit = zvit
#        self.publicacii = publicacii
#        self.kartograph = kartograph
#        self.coord = coord
#        self.tochkart = tochkart
#        self.basejn = basejn
#        self.toppotype = toppotype
#        self.geomorform = geomorform
#        self.vysotnadrm = vysotnadrm
##        self.ploshch = ploshch
#        self.dovz = dovz
#        self.shyr= shyr
#
#    @property #i might have to change this to __init__
#    def serialize(self):
#        """Return object data in easily serializeable format"""
#        return {
#                'name': self.name,
#                'id': self.id,
#                'toponim': self.toponim,
#                'type_of_site': self.type_of_site,
#                'oblast': self.oblast,
#                'rajon': self.rajon,
#                'punkt': self.punkt,
#                'prymitky': self.prymitky,
#                'kultnal': self.kultnal,
#                'chron': self.chron,
#                'nadijnist': self.nadijnist,
#                'rozkop': self.rozkop,
#                'zvit': self.zvit,
#                'publicacii': self.publicacii,
#                'kartograph': self.kartograph,
#                'coord': self.coord,
#                'tochkart': self.tochkart, 
#                'toppotype': self.toppotype,
#                'geomorform': self.geomorform,
#                'vysotnadrm': self.vysotnadrm,
#                'ploshch': self.ploshch,
#                'dovz': self.dovz,
#                'shyr': self.shyr
#                }
    def __repr__(self):
        return '<Site %r>' % self.name

whooshalchemy.whoosh_index(app, Site)

@app.route('/search/<query>', methods=['GET', 'POST'])
def search(query):
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
    else:
        results = Site.query.whoosh_search(query).all()
        return render_template('search.html', results=results)

@app.route('/', methods=['GET', 'POST'])
def welcomePage():
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
    else:
        return render_template('welcome.html')

@app.route('/new', methods=['GET', 'POST'])
def newSite():
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 

        TheNewSite = Site(name=request.form['name'], 
                toponim=request.form['toponim'])
#                type_of_site = request.form['type_of_site'])
#                oblast=request.form['oblast'],
#                rajon=request.form['rajon'],
#                punkt=request.form['punkt'],
#                prymitky=request.form['prymitky'],
#                kultnal=request.form['kultnal'],
#                chron=request.form['chron'],
#                nadijnist=request.form['nadijnist'],
#                rozkop=request.form['rozkop'],
#                zvit=request.form['zvit'],
#                publicacii = request.form['publicacii'],
#                kartograph = request.form['kartograph'],
#                coord = request.form['coord'],
#                tochkart = request.form['tochkart'],
#                toppotype = request.form['toppotype'],
#                geomorform = request.form['geomorform'],
#                vysotnadrm = request.form['vysotnadrm'], 
#                ploshch = request.form['ploshch'],
#                dovz = request.form['dovz'],
#                shyr = request.form['shyr'])
#                
        db.session.add(TheNewSite)
        db.session.commit()
        return redirect(url_for('welcomePage')) 
    else:
        return render_template('newsite.html')


@app.route('/<int:site_id>/', methods = ['GET', 'POST'])
def sitePage(site_id):
    if request.method == 'GET':
        onesite = db.session.query(Site).filter_by(id=site_id).one()

        return render_template('site.html', site=onesite) 
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 

@app.route('/<int:site_id>/edit/', methods = ['GET', 'POST'])
@app.route('/<int:site_id>/edit/base', methods = ['GET', 'POST'])
def siteEdit(site_id):
    siteToEdit = db.session.query(Site).filter_by(id=site_id).one()
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
        if request.form['name']:
            siteToEdit.name = request.form['name']
        if request.form['toponim']:
            siteToEdit.toponim = request.form['toponim']
        if request.form['type_of_site']:
            siteToEdit.type_of_site = request.form['type_of_site']
        if request.form['oblast']:
            siteToEdit.oblast = request.form['oblast']
        if request.form['rajon']:
            siteToEdit.rajon = request.form['rajon']
        if request.form['punkt']:
            siteToEdit.punkt = request.form['punkt']
        if request.form['prymitky']:
            siteToEdit.prymitky = request.form['prymitky']
        if request.form['kultnal']:
            siteToEdit.kultnal = request.form['kultnal']
        if request.form['chron']:
            siteToEdit.chron = request.form['chron']
        if request.form['nadijnist']:
            siteToEdit.nadijnist = request.form['nadijnist']
        if request.form['rozkop']:
            siteToEdit.rozkop = request.form['rozkop']
        if request.form['zvit']:
            siteToEdit.zvit = request.form['zvit']
        if request.form['publicacii']:
            siteToEdit.publicacii = request.form['publicacii']
        if request.form['kartograph']:
            siteToEdit.kartograph = request.form['kartograph']
        if request.form['coord']:
            siteToEdit.coord = request.form['coord']
        if request.form['tochkart']:
            siteToEdit.tochkart = request.form['tochkart']
        if request.form['toppotype']:
            siteToEdit.toppotype = request.form['toppotype']
        if request.form['geomorform']:
            siteToEdit.geomorform = request.form['geomorform']
        if request.form['vysotnadrm']:
            siteToEdit.vysotnadrm = request.form['vysotnadrm']
        if request.form['ploshch']:
            siteToEdit.ploshch = request.form['ploshch']
        if request.form['dovz']:
            siteToEdit.dovz = request.form['dovz']
        if request.form['shyr']:
            siteToEdit.shyr = request.form['shyr']

        db.session.add(siteToEdit)
        db.session.commit()
        return redirect(url_for('sitePage', site_id=site_id))

    else:
        return render_template('edit.html', site=siteToEdit)

@app.route('/<int:site_id>/delete/', methods=['GET', 'POST'])
def siteDelete(site_id):
    siteToDelete = db.session.query(Site).filter_by(id=site_id).one()
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
        db.session.delete(siteToDelete)
        db.session.commit
        return redirect(url_for('welcomePage'))
    else:
        return render_template('delete.html', site=siteToDelete)

@app.route('/all/', methods=['GET', 'POST'])
def allSites():
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
    else:
        sites = db.session.query(Site).all()
        return render_template('all.html', sites=sites)


from archapp import views
