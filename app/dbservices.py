import urllib
import pymongo.mongo_client
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

uri = "mongodb+srv://vinay_da:" + urllib.parse.quote("vinays@123")+"@dota2-agnuc.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
player = client.dotaproj.player
herodetails = client.dotaproj.herodetails
playerhero = client.dotaproj.playerhero
match = client.dotaproj.match
playermatch = client.dotaproj.playermatch
logindetails = client.dotaproj.logindetails


def check_password(self, password, email):
        password_hash=logindetails.find_one({"_id": email}, {"_id": 0, "passowrd_hash": 1, "pid":1})
        hash = generate_password_hash(password_hash['password_hash'])
        j=check_password_hash(hash, password)
        if j:
            @login.user_loader
            def load_user(id):
                return password_hash['pid']

        return j


def set_password(self, password):
    return generate_password_hash(password)
