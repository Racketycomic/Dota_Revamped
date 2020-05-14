from app import app
from flask import render_template, url_for, redirect
from app import dbservices as db
from app.forms import matchbar, heroname
from app.sift import playertable, matchtable
import logging
import os
import yaml


@app.route('/items',methods=['POST','GET'])
def items():
    return render_template('items.html')

@app.route('/heroes',methods=['POST','GET'])
def heroes():
    return render_template('heroes.html')

@app.route('/')
@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/mids', methods=['POST', 'GET'])
def mids():
    form = matchbar()
    matches = form.matchid.data
    if form.validate_on_submit():
        return redirect('midswid/'+str(matches))
    return render_template('newmatch.html', form=form)


@app.route('/midswid/<int:matches>', methods=["POST", "GET"])
def midswid(matches):
    users = db.match.find_one({"_id": matches})
    print("inside mid before if")
    if users == None:
        print("inside the if loop in mids")
        matchdetail = matchtable()
        matchdetail.getmatch(matches)
        users = db.match.find_one({"_id": matches})
        print(users)
        radiant = db.playermatch.find_one({"_id": matches},
                                 {
                                  "kill_count" : {"$slice":5},
                                  "death_count": {"$slice": 5},
                                  "assist_count": {"$slice": 5},
                                  "kdaratio": {"$slice": 5},
                                  "playername": {"$slice": 5},
                                  "xpm": {"$slice": 5}, "gpm": {"$slice": 5},
                                  "team": {"$slice": 5}, "result": {"$slice": 5},
                                  "heroname": {"$slice": 5},"_id":0,"playerid":0
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
        list1=[]
        i=0
        rlist=[]
        while i<5:
            g=radiant.get('playername')
            list1.append(g[i])
            g=radiant.get('heroname')
            list1.append(g[i])
            g=radiant.get('kill_count')
            list1.append(g[i])
            g=radiant.get('death_count')
            list1.append(g[i])
            g=radiant.get('assist_count')
            list1.append(g[i])
            g=radiant.get('kdaratio')
            list1.append(g[i])
            g=radiant.get('xpm')
            list1.append(g[i])
            g=radiant.get('gpm')
            list1.append(g[i])
            print(list1)
            g=radiant.get('result')
            list1.append(g[i])
            rlist.append(list1)
            list1=[]
            i=i+ 1

        list1=[]
        i=0
        dlist=[]
        while i<5:
            g=dire.get('playername')
            list1.append(g[i])
            g=dire.get('heroname')
            list1.append(g[i])
            g=dire.get('kill_count')
            list1.append(g[i])
            g=dire.get('death_count')
            list1.append(g[i])
            g=dire.get('assist_count')
            list1.append(g[i])
            g=dire.get('kdaratio')
            list1.append(g[i])
            g=dire.get('xpm')
            list1.append(g[i])
            g=dire.get('gpm')
            list1.append(g[i])
            g=dire.get('result')
            list1.append(g[i])
            dlist.append(list1)
            list1=[]
            i=i+ 1

        return render_template("matchtable.html", rlist = rlist, dlist=dlist)

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
    list1=[]
    i=0
    rlist=[]
    while i<5:
        g=radiant.get('playername')
        list1.append(g[i])
        g=radiant.get('heroname')
        list1.append(g[i])
        g=radiant.get('kill_count')
        list1.append(g[i])
        g=radiant.get('death_count')
        list1.append(g[i])
        g=radiant.get('assist_count')
        list1.append(g[i])
        g=radiant.get('kdaratio')
        list1.append(g[i])
        g=radiant.get('xpm')
        list1.append(g[i])
        g=radiant.get('gpm')
        list1.append(g[i])
        print(list1)
        g=radiant.get('result')
        list1.append(g[i])
        rlist.append(list1)
        list1=[]
        i=i+ 1

    list1=[]
    i=0
    dlist=[]
    while i<5:
        g=dire.get('playername')
        list1.append(g[i])
        g=dire.get('heroname')
        list1.append(g[i])
        g=dire.get('kill_count')
        list1.append(g[i])
        g=dire.get('death_count')
        list1.append(g[i])
        g=dire.get('assist_count')
        list1.append(g[i])
        g=dire.get('kdaratio')
        list1.append(g[i])
        g=dire.get('xpm')
        list1.append(g[i])
        g=dire.get('gpm')
        list1.append(g[i])
        g=dire.get('result')
        list1.append(g[i])
        dlist.append(list1)
        list1=[]
        i=i+ 1

    return render_template("matchtable.html", users=users, rlist=rlist,
                           dlist=dlist)


@app.route("/herosearch", methods=['POST', 'GET'])
def herosearch():
    form = heroname()
    hero = form.hero.data
    if form.validate_on_submit():
        return (redirect("/heroname/"+str(hero)))
    return render_template("hero_analysis.html", form=form)


@app.route("/heroname/<string:hero>", methods=['POST', 'GET'])
def heros(hero):
    hname =hero

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
    print(hlist)
    return render_template("hero_analysis_result.html", hlist=hlist)

logging.basicConfig(filename='app.log', filemode='a+')
