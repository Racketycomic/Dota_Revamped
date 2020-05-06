from app import app
from flask import render_template,url_for,redirect
from app import dbservices as db
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegisterForm, matchbar
from app.sift import playertable, matchtable

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


def login():
    flag1 = 0
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    print(form.email.data)
    print(form.password.data)
    user = ''
    if form.validate_on_submit():
        print(form.email.data)
        print(form.password.data)
        u = db.logindetails.find_one({"_id": form.email.data}, {"_id": 1})
        u['email'] = user
        if user is None or not db.check_password(form.password.data, form):
            flag1 = 1
            return render_template('login.html', form=form, flag1=flag1)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, flag1=flag1)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    print(form.username.data)
    print(form.email.data)
    if form.validate_on_submit():
        pwd = db.set_password(form.password.data)
        db.logindetails.insert_one({"_id": form.email.data, "pid": form.id.data,
                                    "username": form.username.data,
                                    "password_hash": pwd})
        user1 = playertable()
        user1.getinfo(form.id.data)
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
