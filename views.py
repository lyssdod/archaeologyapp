# -*- coding: utf-8 -*-
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask import render_template, request, url_for, flash, redirect, g
from myapp import app, db 
from forms import newSiteForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from auth import OAuthSignIn, GoogleSignIn
from models import Site, User
from functools import wraps

@app.before_request
def before_request():
    g.user = current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash('Ви вже увійшли')
        return redirect(url_for('welcomePage'))
    return render_template('login.html', title='Sign In')


@app.route('/logout')
def logout():
    logout_user()
    flash('Користувач вийшов')
    return redirect(url_for('welcomePage'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('welcomePage'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('welcomePage'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        flash('Помилка автентифікації')
        return redirect(url_for('welcomePage'))
    user = User.query.filter_by(email=email).first()
    if not user:
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]
        user=User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, remember=True)
    flash('Увійшли як %s'% user.nickname)
    return redirect(url_for('welcomePage'))

@app.route('/', methods=['GET', 'POST'])
def welcomePage():
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
    else:
        return render_template('welcome.html')
@app.route('/gmap', methods=['GET' ])
def gmap():
    if request.method == 'GET':
        return render_template('gmap.html')


@app.route('/new', methods=['GET', 'POST'])
@login_required
def newSite():
    form= newSiteForm()
    if form.validate_on_submit():
        flash('Added the new Site "%s"' % 
                (form.name.data))

        TheNewSite = Site(name=request.form['name'], 
                toponim=request.form['toponim'],
                type_of_site = request.form['type_of_site'],
                krajina=request.form['krajina'],
                oblast=request.form['oblast'],
                rajon=request.form['rajon'],
                punkt=request.form['punkt'],
                pryvjazka=request.form['pryvjazka'],
                skiph=request.form.get('skiph'),
                juhn=request.form.get('juhn'),
                pjuhn=request.form.get('pjuhn'),
                verok=request.form.get('verok'),
                dvosh=request.form.get('dvosh'),
                drz=request.form.get('drz'),
                localgr=request.form['localgr'],
                chron=request.form['chron'],
                nadijnist=request.form['nadijnist'],
                rozkop=request.form.get('rozkop'),
                dospl=request.form['dospl'],
                zvit=request.form['zvit'],
                publicacii = request.form['publicacii'],
                kartograph = request.form.get('kartograph'),
                latd = request.form['latd'],
                longt = request.form['longt'],
                tochkart = request.form['tochkart'],
                basejn = request.form['basejn'],
                toppotype = request.form['toppotype'],
                geomorform = request.form['geomorform'],
                vysotnadrm = request.form['vysotnadrm'], 
                ploshch = request.form['ploshch'],
                dovz = request.form['dovz'],
                shyr = request.form['shyr'],
                foto = request.form.get('foto'),
                plans = request.form.get('plans'), 
                znahidky = request.form.get('znahidky'),
                kistka = request.form.get('kistka'),
                zalizo= request.form.get('zalizo'),
                kamin = request.form.get('kamin'),
                glyna= request.form.get('glyna'),
                prymitky=request.form.get('prymitky')
               )
        db.session.add(TheNewSite)
        db.session.commit()
        return redirect(url_for('allSites')) 
    else:
        return render_template('newsite.html', title="Нова пам'ятка", form=form)

    if request.method == 'POST':
        if request.form.get('name_of_site', None):
            results = request.form['name_of_site']
            return redirect(url_for('search', query=results)) 
        else:
            return render_template('newsite.html', title="New Site", form=form)


@app.route('/<int:site_id>/', methods = ['GET', 'POST'])
def sitePage(site_id):
    if request.method == 'GET':
        onesite = db.session.query(Site).filter_by(id=site_id).one()
        usr = db.session.query(User).filter_by(id=1).one()
        return render_template('site.html', site=onesite, user=usr) 
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
        if request.form.get("name_of_site"):
            results = request.form.get("name_of_site")
            return redirect(url_for('search', query=results)) 
        if request.form.get('Delete'):
            db.session.delete(siteToDelete)
            db.session.commit()
            print "site has been deleted"
        return redirect(url_for('welcomePage'))
    else:
        return render_template('delete.html', site=siteToDelete)

@app.route('/all/', methods=['GET', 'POST'])
def allSites():
    if request.method == 'POST':
        if request.form.get("name_of_site", None):
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
        else:
            sites = db.session.query(Site).all()
            if request.form.get('kistka'):
                kistka = request.form.get('kistka')
                sort_kistka = Site.query.filter_by(kistka = kistka).all()
                sites = [x for x in sites if x in sort_kistka]
            if request.form.get('zalizo'):
                zalizo = request.form.get('zalizo')
                sort_zalizo = Site.query.filter_by(zalizo = zalizo).all()
                sites = [x for x in sites if x in sort_zalizo]
            if request.form.get('kamin'):
                kamin = request.form.get('kamin')
                sort_kamin = Site.query.filter_by(kamin = kamin).all()
                sites = [x for x in sites if x in sort_kamin]
            if request.form.get('glyna'):
                glyna = request.form.get('glyna')
                sort_glyna = Site.query.filter_by(glyna = glyna).all()
                sites = [x for x in sites if x in sort_glyna]
            if request.form['by_type']:
                type_of_site = request.form.get('by_type')
                sort_type = Site.query.filter_by(type_of_site=type_of_site).all()
                sites = [x for x in sites if x in sort_type]
            if request.form['oblast']:
                oblast = request.form['oblast']
                sort_obl = Site.query.filter_by(oblast=oblast).all()
                sites = [x for x in sites if x in sort_obl]
            if request.form['rajon']:
                rajon = request.form['rajon']
                sort_rajon = Site.query.filter_by(rajon=rajon).all()
                sites = [x for x in sites if x in sort_rajon]
            if request.form['basejn']:
                basejn = request.form['basejn']
                sort_basejn = Site.query.filter_by(basejn=basejn).all()
                sites = [x for x in sites if x in sort_basejn]
            if request.form['kultnal']:
                kultnal = request.form['kultnal']
                sort_kultnal = Site.query.filter_by(kultnal=kultnal).all()
                sites = [x for x in sites if x in sort_kultnal]
            if request.form['toppotype']:
                toppotype= request.form.get('toppotype')
                sort_toppotype = Site.query.filter_by(toppotype=toppotype).all()
                sites = [x for x in sites if x in sort_toppotype]
            if request.form.get('rozkop'):
                rozkop = request.form.get('rozkop')
                sort_rozkop = Site.query.filter_by(rozkop=rozkop).all()
                sites = [x for x in sites if x in sort_rozkop]
            if request.form.get('dodatky'):
                sort_dodatky=[]
                for e in db.session.query(Site).all():
                    value = u'Є'
                    if e.foto==value or e.plans==value or e.znahidky==value:
                        sort_dodatky.append(e)
                sites = [x for x in sites if x in sort_dodatky]
            if request.form.get('vysota'):
                vysotnadrm = request.form.get('vysota')
                val = vysotnadrm.split(',', 1)
                minval = int(val[0])
                maxval = int(val[1])
                vysotmin = Site.query.filter(Site.vysotnadrm >= minval).all()
                vysotmax = Site.query.filter(Site.vysotnadrm <= maxval).all()
                sites = [x for x in sites if x in vysotmin]
                sites = [x for x in sites if x in vysotmax]
            if request.form.get('ploshcha'):
                ploshcha = request.form.get('ploshcha')
                val = ploshcha.split(',', 1)
                minval = int(val[0])
                maxval = int(val[1])
                plmin = Site.query.filter(Site.ploshch >= minval).all()
                plmax = Site.query.filter(Site.ploshch <= maxval).all()
                sites = [x for x in sites if x in plmin]
                sites = [x for x in sites if x in plmax]

            if request.form.get("by_alphabet"):
                sorted_sites = sites.sort(key=lambda x: x.name)
            return render_template('all.html', sites=sites)
    else:
        sites = db.session.query(Site).all()
        return render_template('all.html', sites=sites, slidebar = True)

@app.route('/search/<query>', methods=['GET', 'POST'])
def search(query):
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
    else:
        results = Site.query.whoosh_search(query).all()
        return render_template('search.html', results=results)

