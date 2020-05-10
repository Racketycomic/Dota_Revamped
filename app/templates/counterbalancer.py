import os
import yaml
import urllib
import pymongo.mongo_client
import pymongo
import json
import time
uri = "mongodb+srv://vinay_da:" + urllib.parse.quote("vinays@123")+"@dota2-agnuc.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
match = client.dotaproj.playermatch


class cbparse():

    def parsefun():
        while(1):
            direct = os.path.join("F:\\drev\\app\\files", "counterfile.txt")
            matchfile = os.path.join("F:\\drev\\app\\files", "playermatch.txt")
            mlist = []
            with open(direct, "r+") as file:
                rstring = file.read()
                rlist = yaml.safe_load(rstring)
                for i in rlist:
                    if i['threshold'] >= 0.01:
                        mlist.append(i['mid'])
            with open(matchfile, "r+") as file:
                rstring = file.read()
                rstring = rstring[:-2]
                rstring = '['+rstring+']'
                rlist = yaml.safe_load(rstring)
                for i in rlist:
                    for index, items in enumerate(mlist):
                        if i['_id'] == items:
                            mlist.pop(index)
            if len(mlist) != 0:
                for i in mlist:
                    playermatch = os.path.join("F:\\drev\\app\\files", "playermatch.txt")
                    mongoresult = playermatch.find_one({"_id": i})
                    mresultstr = json.dumps(mongoresult, indent=-1)
                    pmfile = open(playermatch, "a+")
                    k = pmfile.tell()
                    d = pmfile.write(mresultstr+"\n,\n")
                    indexdict = {"matchid": i, "spos": k, "size": d}
                    indexdstr = json.dumps(indexdict, indent=-1)
                    indexfile = open("playermatch_index.txt", "a+")
                    indexfile.write(indexdstr+"\n,\n")
                    indexfile.close()
                    pmfile.close()
            time.sleep(60)
