import urllib
import pymongo.mongo_client
import pymongo
from werkzeug.security import generate_password_hash, check_password_hash

password=""
username=""
uri = "mongodb+srv://{username}:" + urllib.parse.quote("{password}")+"@dota2-agnuc.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
player = client.dotaproj.player
herodetails = client.dotaproj.herodetails
playerhero = client.dotaproj.playerhero
match = client.dotaproj.match
playermatch = client.dotaproj.playermatch
logindetails = client.dotaproj.logindetails


class crud(): 

    def login(username,password): 
        userdoc = logindetails.find_one({'_id':username})
        if userdoc == None: 
            return False 
        else: 
            if check_password_hash(userdoc['password_hash'], password):
                return True
            else: 
                return False

    def register(username,email,pid,password):
        userdoc = logindetails.find_one({'_id':email})
        if userdoc == None:
            passwordhash = generate_password_hash(password)
            document = {'_id':email,'username':username,'pid':pid,'password_hash':passwordhash}
            logindetails.insert_one(document)
            return True
        else: 
            return False
