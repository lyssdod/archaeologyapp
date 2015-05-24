from flask import Flask

app=Flask(__name__)

@app.route('/')
def welcomePage():
    return 'This is the welcome page'

@app.route('/new')
def newSite():
    return 'This is the new page'

@app.route('/<int:site_id>/')
def sitePage(site_id):
    return 'This is the site page'

@app.route('/<int:site_id>/edit/')
def siteEdit(site_id):
    return 'This is the page for editing the site'

@app.route('/<int:site_id>/delete/')
def siteDelete(site_id):
    return 'This is the page for deleting the site'

@app.route('/all/')
def allSites():
    return 'This is the page for all sites'




if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
