from flask import render_template, url_for, redirect,Flask,session,request
from dbservices import crud
import dbservices as db
from sift import playertable, matchtable
import logging
import os
import yaml
from forms import matchvalidations
from werkzeug.security import generate_password_hash, check_password_hash



filepath="/home/vinay/fsproject2/app/files"

app = Flask(__name__)
app.secret_key = 'super secret key'
# @app.route('/items',methods=['POST','GET'])
# def items():
#     return render_template('items.html')

# @app.route('/heroes',methods=['POST','GET'])
# def heroes():
#     return render_template('heroes.html')

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('homepage_blog.html',session=session)

@app.route('/updates')
def updates():
    return render_template('homepage_updates.html',session=session)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(password)
        session.pop('user_id', None)
        doc = crud.login(username, password)
       
        if not doc:
            error = 'Your email or password is wrong'
            print(error)
            return render_template('login.html', error=error)
        else:
            session['user_id'] = username
            return render_template('homepage_blog.html',session=session)
    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register(): 
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repass = request.form['repass']
        pid = int(request.form['playerid'])
        if password != repass:
            return render_template('register.html')
        else:
            succ = crud.register(username, email, pid, password)
            if succ: 
                return redirect('login')
            else:
                return redirect('register')
        if len(doc) != 0:
            error = "The email already exists"
            render_template('register.html', error=error)
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return render_template('homepage_blog.html',session=session)

@app.route('/mids', methods=['POST', 'GET'])
def mids():
    if request.method == 'POST':
        matchid = request.form['match_id']
        if matchvalidations.validate_matchid(matchid):
            return redirect('midswid/'+str(matchid))
    return render_template('match_id_analysis.html')


@app.route('/midswid/<int:matches>', methods=["POST", "GET"])
def midswid(matches):
    users = db.match.find_one({"_id": matches})
    if users == None:
        matchdetail = matchtable()
        matchdetail.getmatch(matches)
        users = db.match.find_one({"_id": matches})
    radiant = db.playermatch.find_one({"_id": matches},
                            {
                            "kill_count" : {"$slice":5},
                            "death_count": {"$slice": 5},
                            "assist_count": {"$slice": 5},
                            "playername": {"$slice": 5},
                            "xpm": {"$slice": 5}, "gpm": {"$slice": 5},
                            "result": {"$slice": 5},
                            "heroname": {"$slice": 5},"_id":0,"playerid":0
                            })

    dire = db.playermatch.find_one({"_id": matches},
                                {
                                "kill_count": {"$slice": -5},
                                "death_count": {"$slice": -5},
                                "assist_count": {"$slice": -5},
                                "playername": {"$slice": -5},
                                "xpm": {"$slice": -5}, "gpm": {"$slice": -5},
                                "team": {"$slice": -5}, "result": {"$slice": -5},
                                "heroname": {"$slice": -5}
                                })

    for i in range(5): 
        print(radiant['playername'][i])

    return render_template("match_id_analysis_result.html", matches=matches,dire=dire,radiant=radiant,users=users)

    

# @app.route("/herosearch", methods=['POST', 'GET'])
# def herosearch():
#     form = heroname()
#     hero = form.hero.data
#     if form.validate_on_submit():
#         return (redirect("/heroname/"+str(hero)))
#     return render_template("hero_analysis.html", form=form)


# @app.route("/heroname/<string:hero>", methods=['POST', 'GET'])
# def heros(hero):
#     hname =hero

#     playermatch = os.path.join(filepath, "player_match_sec_hero.txt")
#     with open(playermatch, "r+") as file:
#         rstring = file.read()
#         rstring = rstring[:-2]
#         rstring = '['+rstring+']'
#         rlist = yaml.safe_load(rstring)
#         hlist = []
#         for i in rlist:
#             for key, values in i.items():
#                 if key == hname:
#                     hlist = values
#     print(hlist)
#     return render_template("hero_analysis_result.html", hlist=hlist)


logging.basicConfig(filename='app.log', filemode='a+')
