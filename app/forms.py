from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
import requests
from app import dbservices as db
import os
import yaml


class matchbar(FlaskForm):
    matchinfo = SubmitField("GETMATCH")
    matchid = IntegerField("Match ID", validators=[DataRequired()])

    def validate_matchid(self, matchid):
        req = requests.get(f"https://api.opendota.com/api/matches/{matchid.data}")
        js = req.json()
        print(js)
        for key, values in js.items():
            if key == "error":
                raise ValidationError("Please enter a valid MatchID")


class heroname(FlaskForm):
    heroclick = SubmitField("Search")
    hero = StringField("Hero name", validators=[DataRequired()])

    def validate_hero(self, hero):
        playermatch = os.path.join("F:\\drev\\app\\files", "player_match_sec_hero.txt")
        j = 0
        with open(playermatch, "r+") as file:
            rstring = file.read()
            rstring = rstring[:-2]
            rstring = '['+rstring+']'
            rlist = yaml.safe_load(rstring)
            for i in rlist:
                for key, values in i.items():
                    if key == hero.data:
                        j = 1
                        break
        if not j:
            raise ValidationError("Hero not available")
