from myapp import app 
if __name__ == '__main__':
    app.debug = True
#    context = ('ssl.crt', 'ssl.key')
    app.run(host='0.0.0.0', port=5000)#, ssl_context=context)
