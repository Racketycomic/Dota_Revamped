import urllib
import pymongo.mongo_client
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from app.__init__ import login

uri = "mongodb+srv://vinay_da:" + urllib.parse.quote("vinays@123")+"@dota2-agnuc.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
player = client.dotaproj.player
herodetails = client.dotaproj.herodetails
playerhero = client.dotaproj.playerhero
match = client.dotaproj.match
playermatch = client.dotaproj.playermatch
logindetails = client.dotaproj.logindetails
