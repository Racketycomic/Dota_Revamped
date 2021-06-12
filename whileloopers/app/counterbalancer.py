import os
import yaml
import urllib
import pymongo.mongo_client
import pymongo
import json
uri = "mongodb+srv://vinay_da:" + urllib.parse.quote("vinays@123")+"@dota2-agnuc.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
match = client.dotaproj.playermatch

filepath ="/home/vinay/fsproject2/app/files"
class cbparse():

    def parsefun(self):
            print("In cbparse")
            direct = os.path.join(filepath, "counterfile.txt")
            matchfile = os.path.join(filepath, "playermatch.txt")
            indfile = os.path.join(filepath, "playermatch_index.txt")
            mlist = []
            k=0
            finallist =[]
            with open(matchfile, "r+") as file:
                rstring = file.read()
                rstring = rstring[:-2]
                rstring = '['+rstring+']'
                mlist = yaml.safe_load(rstring)
                l = len(mlist)
                if l < 10:
                    k = 10-l

            with open(indfile, "r+") as file:
              rstring = file.read()
              rstring = rstring[:-2]
              rstring ='['+rstring+']'
              indlist = yaml.safe_load(rstring)
              if len(indlist) != 0:
                  indlist = sorted(indlist,key=lambda i:i['threshold'])

            with open(direct,"r+") as file:
                rstring = file.read()
                addlist = yaml.safe_load(rstring)
                if len(indlist) != 0:
                    addlist = sorted(addlist, key=lambda i: i['threshold'], reverse=True)

            if addlist is None:
                with open(direct, "a+") as file:
                    rstring = file.read()
                    rlist = yaml.safe_load(rstring)
                    for i in rlist:
                        mongoresult = match.find_one({'_id': i['mid']})
                        mresultstr = json.dumps(mongoresult, indent=-1)
                        j = file.tell()
                        d = file.write(mresultstr+"\n,\n")
                        indexdict = {"matchid": i['mid'], "spos": j, "size": d,
                                     "threshold": i['threshold']}
                        indexdstr = json.dumps(indexdict, indent=-1)
                        indexfile = open(indfile, "a+")
                        indexfile.write(indexdstr+"\n,\n")
                        indexfile.close()
            else:
                l2 = len(addlist)
                if l2 < k:
                    k = l2
                if k>0:
                    i=0
                    while i < k:
                        finallist.append(addlist[i])
                        i = i+1
                    with open(matchfile, "a+") as file:
                        for i in finallist:
                            mongoresult = match.find_one({'_id': i['mid']})
                            mresultstr = json.dumps(mongoresult, indent=-1)
                            j = file.tell()
                            d = file.write(mresultstr+"\n,\n")
                            indexdict = {"matchid": i['mid'], "spos": j, "size": d,
                                         "threshold": i['threshold']}
                            indexdstr = json.dumps(indexdict, indent=-1)
                            indexfile = open(indfile, "a+")
                            indexfile.write(indexdstr+"\n,\n")
                        indexfile.close()
                if k == 0:
                    kickid = indlist[0]
                    enterid = addlist[0]
                    spos = 0
                    size = 0
                    with open(indfile,"r+") as file:
                        rstring = file.read()
                        rstring = rstring[:-2]
                        rstring ='['+rstring+']'
                        blist = yaml.safe_load(rstring)
                        for i in blist:
                            if i['matchid'] == kickid:
                                i['matchid'] = enterid
                                spos = i['spos']
                                size = i['size']
                    with open(matchfile,"a+") as file:
                       file.seek(spos)
                       mongoresult = match.find_one({'_id': enterid})
                       mresultstr = json.dumps(mongoresult, indent=-1)
                       file.write(mresultstr)
