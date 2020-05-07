from app import app
from flask import render_template, url_for,redirect
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
        u = db.logindetails.find_one({"_id": form.email.data}, {"_id": 1})
        user = u['email']
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


@app.route('/performance', methods=['GET', 'POST'])
def performance():
    id = current_user.get_id()
    user = db.playerhero.find_one({"_id":id}, {"performance":1,"heroname":1,"_id":0})
    return render_template('performance.html',user=user)


@app.route('/mids',methods=['POST','GET'])

def mids():
    form=matchbar()
    matches=form.matchid.data
    if form.validate_on_submit():
        return redirect('midswid/'+str(matches))
    return render_template('newmatch.html',form=form)

@app.route('/midswid/<int:matches>',methods=["POST","GET"])
def midswid(matches):
    users = db.match.find_one({"_id": matches})
    print("inside mid before if")
    if len(users) == 0:
        print("inside the if loop in mids")
        matchdetail = matchtable()
        matchdetail.getmatch(matches)
        users = db.match.find_one({"_id": matches })
        radiant= db.playermatch.find_one({"_id": matches},
                                 {"playerid": {"$slice": 5} , "kill_count": {"$slice": 5},
                                  "death_count": {"$slice": 5}, "assist_count": {"$slice": 5},
                                  "kdaratio": {"$slice": 5}, "playername": {"$slice": 5},
                                  "xpm": {"$slice": 5}, "gpm": {"$slice": 5},
                                  "team": {"$slice": 5}, "result": {"$slice": 5},
                                  "heroname": {"$slice": 5}
                                    })
        dire = db.playermatch.find_one({"_id": 4305164363},
                                 {"playerid": {"$slice": -5} , "kill_count": {"$slice": -5},
                                  "death_count": {"$slice": -5}, "assist_count": {"$slice": -5},
                                  "kdaratio": {"$slice": -5}, "playername": {"$slice": -5},
                                  "xpm": {"$slice": -5}, "gpm": {"$slice": -5},
                                  "team": {"$slice": -5}, "result": {"$slice": -5},
                                  "heroname": {"$slice": -5}
                                    })
        return render_template("matchtable.html",users=users,radiant=radiant,dire=dire)


        radiant = db.playermatch.find_one({"_id": matches},
                             {"playerid": {"$slice": 5} , "kill_count": {"$slice": 5},
                              "death_count": {"$slice": 5}, "assist_count": {"$slice": 5},
                              "kdaratio": {"$slice": 5}, "playername": {"$slice": 5},
                              "xpm": {"$slice": 5}, "gpm": {"$slice": 5},
                              "team": {"$slice": 5}, "result": {"$slice": 5},
                              "heroname": {"$slice": 5}
        dire = db.playermatch.find_one({"_id": matches},
                             {"playerid": {"$slice": -5} , "kill_count": {"$slice": -5},
                              "death_count": {"$slice": -5}, "assist_count": {"$slice": -5},
                              "kdaratio": {"$slice": -5}, "playername": {"$slice": -5},
                              "xpm": {"$slice": -5}, "gpm": {"$slice": -5},
                              "team": {"$slice": -5}, "result": {"$slice": -5},
                              "heroname": {"$slice": -5}}
                                        )
    return render_template('matchtable.html', users=users, radiant=radiant, dire=dire)
