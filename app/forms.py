from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
import requests
import dbservices as db
import os
import yaml
import json

filepath="/home/vinay/fsproject/app/files"


class matchvalidations():
    def validate_matchid(matchid):
        req = requests.get(f"https://api.opendota.com/api/matches/{matchid}")
        js = req.json()
        for key, values in js.items():
            if key == "error":
                return False
            else:
                return True


# class matchbar(FlaskForm):
#     matchinfo = SubmitField("GETMATCH")
#     matchid = IntegerField("Match ID", validators=[DataRequired()])

#     def validate_matchid(self, matchid):

#         req = requests.get(f"https://api.opendota.com/api/matches/{matchid.data}")
#         js = req.json()
#         print(js)
#         for key, values in js.items():
#             if key == "error":
#                 raise ValidationError("Please enter a valid MatchID")


class heroname(FlaskForm):
    heroclick = SubmitField("Search")
    hero = StringField("Heroname", validators=[DataRequired()])

    def validate_hero(self, hero):
        t=0
        playermatch = os.path.join(filepath, "player_match_sec_hero.txt")
        match = os.path.join(filepath, "playermatch1.txt")
        mlist = []
        j = False
        flag = 0
        with open(playermatch, "r+") as file:
            rstring = file.read()
            rstring = rstring[:-2]
            rstring = '['+rstring+']'
            rlist = yaml.safe_load(rstring)
            for i in rlist:
                for key, values in i.items():
                    if key == hero.data:
                        j = True
                        flag = 0
                        break
        print(j)
        if not j:
            with open(match,"r+") as file:
                rstring = file.read()
                rstring = rstring[:-2]
                rstring = '['+rstring+']'
                rlist = yaml.safe_load(rstring)
                for k in rlist:
                    for key, values in k.items():
                        if key == "_id":
                            mid = values
                        if key == "heroname":
                            for u in values:
                                if u == hero.data:
                                    mlist.append(mid)
                                    continue
            for index, items in enumerate(mlist):
                for index1, items1 in enumerate(mlist):
                    if index == index1:
                        pass
                    if items == items1:
                        mlist.pop(index)
            print(mlist)
            mdict ={hero.data:mlist}
            mdict = json.dumps(mdict, indent=-1)
            type(mdict)
            with open(playermatch, "a+") as file:
                file.write(mdict+"\n,\n")
            if len(mlist) == 0:
                flag = 1
        if flag:
            raise ValidationError("Hero is not present")
