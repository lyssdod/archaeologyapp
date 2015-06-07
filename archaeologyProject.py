from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Site

app=Flask(__name__)

engine = create_engine('sqlite:///thesite.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#myFirstSite = Site(name = "Dark Lake")
#session.add(myFirstSite)
#session.commit()
#firstResult = session.query(Site).first()
#print firstResult.name

#thesite = {'name': 'Death Cemetary', 'id': '1'}

@app.route('/')
def welcomePage():
    return render_template('welcome.html')

@app.route('/new', methods=['GET', 'POST'])
def newSite():
    if request.method == 'POST':
        TheNewSite = Site(name=request.form['name'], 
                toponim=request.form['toponim'],
                type_of_site = request.form['type_of_site'],
                oblast=request.form['oblast'],
                rajon=request.form['rajon'],
                punkt=request.form['punkt'],
                prymitky=request.form['prymitky'],
                kultnal=request.form['kultnal'],
                chron=request.form['chron'],
                nadijnist=request.form['nadijnist'],
                rozkop=request.form['rozkop'],
                zvit=request.form['zvit'],
                publicacii = request.form['publicacii'],
                kartograph = request.form['kartograph'],
                coord = request.form['coord'],
                tochkart = request.form['tochkart'],
                toppoltype = request.form['toppoltype'],
                geomorform = request.form['geomorform'],
                vysotnadrm = request.form['vysotnadrm'], 
                ploshch = request.form['ploshch'],
                dovz = request.form['dovz'],
                shyr = request.form['shyr'])
                
        session.add(TheNewSite)
        session.commit()
        return redirect(url_for('welcomePage')) 
    else:
        return render_template('newsite.html')


@app.route('/<int:site_id>/', methods = ['GET', 'POST'])
def sitePage(site_id):
    if request.method == 'GET':
        onesite = session.query(Site).filter_by(id=site_id).one()
        name = onesite.name
        toponim = onesite.toponim
        type_of_site = onesite.type_of_site
        oblast = onesite.oblast
        rajon = onesite.rajon
        punkt = onesite.punkt
        prymitky = onesite.prymitky
        kultnal = onesite.kultnal
        chron = onesite.chron
        nadijnist = onesite.nadijnist
        rozkop = onesite.rozkop
        zvit = onesite.zvit
        publicacii = onesite.publicacii
        kartograph = onesite.kartograph
        coord = onesite.coord
        tochkart = onesite.tochkart
        toppoltype = onesite.toppoltype
        geomorform = onesite.geomorform
        vysotnadrm = onesite.vysotnadrm
        ploshch = onesite.ploshch
        dovz = onesite.dovz
        shyr = onesite.shyr

        return render_template('site.html', name=name, toponim = toponim,
            type_of_site = type_of_site, oblast=oblast, rajon=rajon, 
            punkt=punkt, prymitky=prymitky, kultnal=kultnal, chron=chron, 
            nadijnist=nadijnist, rozkop=rozkop, zvit=zvit, 
            publicacii=publicacii, kartograph=kartograph, coord=coord,
            tochkart=tochkart, toppoltype=toppoltype, geomorform=geomorform,
            vysotnadrm=vysotnadrm, ploshch=ploshch, dovz=dovz, 
            shyr=shyr, site=onesite) 
        if request.method == 'POST':
            return None

@app.route('/<int:site_id>/edit/', methods = ['GET', 'POST'])
@app.route('/<int:site_id>/edit/base', methods = ['GET', 'POST'])
def siteEdit(site_id):
    siteToEdit = session.query(Site).filter_by(id=site_id).one()
    if request.method == 'POST':
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
        if request.form['toppoltype']:
            siteToEdit.toppoltype = request.form['toppoltype']
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

        session.add(siteToEdit)
        session.commit()
        return redirect(url_for('sitePage', site_id=site_id))

    else:
        return render_template('edit.html', site=siteToEdit)

@app.route('/<int:site_id>/delete/', methods=['GET', 'POST'])
def siteDelete(site_id):
    siteToDelete = session.query(Site).filter_by(id=site_id).one()
    if request.method == 'POST':
        session.delete(siteToDelete)
        session.commit
        return redirect(url_for('welcomePage'))
    else:
        return render_template('delete.html', site=siteToDelete)

@app.route('/all/')
def allSites():
    sites = session.query(Site).all()
    return render_template('all.html', sites=sites)

#sites = session.query(Site).all()
#for site in sites:
 #   print site.name
#thesite = session.query(Site).filter_by(id=1).one()
#print thesite.name


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
