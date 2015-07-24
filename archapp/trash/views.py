from flask import render_template, request, url_for, flash, redirect
from myapp import app, db 
from forms import LoginForm
from flask import session as login_session
import random, string
from models import Site

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "archaeology app"


# Create anti-forgery state token
@app.route('/oauth')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('oath.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


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


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' % 
                (form.openid.data, str(form.remember_me.data)))
        return redirect(url_for('welcome'))
    return render_template('login.html', title="Sign in", form=form)

@app.route('/search/<query>', methods=['GET', 'POST'])
def search(query):
    if request.method == 'POST':
        if request.form["name_of_site"]:
            results = request.form["name_of_site"]
            return redirect(url_for('search', query=results)) 
    else:
        results = Site.query.whoosh_search(query).all()
        return render_template('search.html', results=results)

