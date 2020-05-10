from app import app
from flask import render_template, url_for, redirect
from app import dbservices as db
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm, matchbar, heroname
from app.sift import playertable, matchtable
import logging
import os
import yaml


@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('homepage_blog.html')


@app.route('/update', methods=['POST', 'GET'])
def update():
    return render_template('homepage_updates.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    flag1 = 0
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
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
        db.logindetails.insert_one({"_id": form.email.data,
                                    "pid": form.id.data,
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


@login_required
@app.route('/performance', methods=['GET', 'POST'])
def performance():
    id = current_user.get_id()
    user = db.playerhero.find_one({"_id": id}, {"performance": 1,
                                                "heroname": 1, "_id": 0})
    return render_template('performance.html', users=user)


@login_required
@app.route('/mids', methods=['POST', 'GET'])
def mids():
    form = matchbar()
    matches = form.matchid.data
    if form.validate_on_submit():
        return redirect('midswid/'+str(matches))
    return render_template('match_id_analysis.html', form=form)


@app.route('/midswid/<int:matches>', methods=["POST", "GET"])
def midswid(matches):
    matches = 4305164363
    users = db.match.find_one({"_id": matches})
    print("inside mid before if")
    if len(users) == 0:

        print("inside the if loop in mids")
        matchdetail = matchtable()
        matchdetail.getmatch(matches)
        users = db.match.find_one({"_id": matches})
        print(users)
        radiant = db.playermatch.find_one({"_id": matches},
                                 {
                                  "kill_count": {"$slice": 5},
                                  "death_count": {"$slice": 5},
                                  "assist_count": {"$slice": 5},
                                  "kdaratio": {"$slice": 5},
                                  "playername": {"$slice": 5},
                                  "xpm": {"$slice": 5}, "gpm": {"$slice": 5},
                                  "team": {"$slice": 5}, "result": {"$slice": 5},
                                  "heroname": {"$slice": 5}, "_id": 0, "playerid": 0
                                    })
        dire = db.playermatch.find_one({"_id": matches},
                                 {
                                  "kill_count": {"$slice": -5},
                                  "death_count": {"$slice": -5},
                                  "assist_count": {"$slice": -5},
                                  "kdaratio": {"$slice": -5},
                                  "playername": {"$slice": -5},
                                  "xpm": {"$slice": -5}, "gpm": {"$slice": -5},
                                  "team": {"$slice": -5}, "result": {"$slice": -5},
                                  "heroname": {"$slice": -5}
                                    })
        print(radiant)
        for key, values in radiant.items():
                if key == "playername":
                    for j in values:
                        g=j
        return render_template("match_id_analysis_result.html", users=users, radiant=radiant, dire=dire)


    radiant = db.playermatch.find_one({"_id": matches},
                             {"playerid": {"$slice": 5} , "kill_count": {"$slice": 5},
                              "death_count": {"$slice": 5}, "assist_count": {"$slice": 5},
                              "kdaratio": {"$slice": 5}, "playername": {"$slice": 5},
                              "xpm": {"$slice": 5}, "gpm": {"$slice": 5},
                              "team": {"$slice": 5}, "result": {"$slice": 5},
                              "heroname": {"$slice": 5}
                              })
    dire = db.playermatch.find_one({"_id": matches},
                            {
                              "playerid": {"$slice": -5},
                              "kill_count": {"$slice": -5},
                              "death_count": {"$slice": -5},
                              "assist_count": {"$slice": -5},
                              "kdaratio": {"$slice": -5},
                              "playername": {"$slice": -5},
                              "xpm": {"$slice": -5}, "gpm": {"$slice": -5},
                              "team": {"$slice": -5}, "result": {"$slice": -5},
                              "heroname": {"$slice": -5}
                              })
    return render_template("match_id_analysis_result.html", users=users, radiant=radiant,
                           dire=dire)

@login_required
@app.route("/herosearch", methods=['POST', 'GET'])
def herosearch():
    form = heroname()
    hname = form.hero.data
    if form.validate_on_submit():
        return (redirect("/heroname/"+str(hname)))
    return render_template("hero_analysis.html", form=form)


@app.route("/heroname/<string:hname>", methods=['POST', 'GET'])
def hero():
    form = heroname()
    hname = form.hero.data
    playermatch = os.path.join("F:\\drev\\app\\files", "player_match_sec_hero.txt")
    with open(playermatch, "r+") as file:
        rstring = file.read()
        rstring = rstring[:-2]
        rstring = '['+rstring+']'
        rlist = yaml.safe_load(rstring)
        hlist = []
        for i in rlist:
            for key, values in i.items():
                if key == hname:
                    hlist = values
    return render_template("hero_analysis_result.html", hlist=hlist)


logging.basicConfig(filename='app.log', filemode='a+')
