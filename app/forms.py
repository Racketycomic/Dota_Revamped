from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
import requests
from app import dbservices as db
import os
import yaml


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
    matchid = StringField("match")
    matchinfo = StringField("mat")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Retype Password", validators=[DataRequired(), EqualTo('password')])
    email = StringField("Email", validators=[DataRequired(), Email()])
    id = IntegerField("Player ID", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = db.logindetails.find_one({"_id": email.data})
        if user is not None:
            raise ValidationError("This email is already registered")

    def validate_id(self,id):
        user = db.logindetails.find_one({"id": id.data})
        if user is not None:
            raise ValidationError("This id is already registered")
        aid = 0
        list1 = []
        re1 = requests.get(f"https://api.opendota.com/api/players/{id.data}")
        js1 = re1.json()
        print(js1)
        for key, values in js1.items():
            if key == 'profile':
                list1.append(values)

        print(list1)
        for i in list1:
            if i['account_id']:
                aid = i['account_id']


        print(aid)

        if id.data != aid:
            raise ValidationError("Please enter a valid PlayerID")


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
