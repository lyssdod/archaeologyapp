from myapp import app 
from werkzeug.serving import run_simple 
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
