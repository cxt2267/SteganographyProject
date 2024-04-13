@bp.route('/login/<email>/<password>')
def login(email, password):
    user = DB.checkUser(email, password)
    if user != "user not found":
        return render_template('index.html', user = user)
    else:
        return render_template('login.html', user = user)