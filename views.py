from archaeologyProject import app

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title="Sign in", form=form)


