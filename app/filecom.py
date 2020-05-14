from app import dbservices as db
import json
import yaml
import os

class fil():

    def matchwrite(self, matchid):
        playermatch = os.path.join("F:\\drev\\app\\files", "playermatch.txt")
        mongoresult = db.playermatch.find_one({"_id": matchid})
        mresultstr = json.dumps(mongoresult, indent=-1)
        pmfile = open(playermatch, "a+")
        k = pmfile.tell()
        d = pmfile.write(mresultstr+"\n,\n")
        indexdict = {"matchid": matchid, "spos": k, "size": d}
        indexdstr = json.dumps(indexdict, indent=-1)
        indexfile = open("playermatch_index.txt", "a+")
        indexfile.write(indexdstr+"\n,\n")
        indexfile.close()
        pmfile.close()
        q = "Record is written to file"
        return (q)

    def matchread(self, matchid):
        playermatch_index = os.path.join("F:\\drev\\app\\files",
                                         "playermatch_index.txt")
        indexfile = open(playermatch_index, "r+")
        rstring = indexfile.read()
        rstring = rstring[:-2]
        rstring = '['+rstring+']'
        rdict = yaml.safe_load(rstring)
        print(rdict)
        for i in rdict:
            if i['matchid'] == matchid:
                startpos = i['spos']
                size = i['size']
        indexfile.close()
        pmfile = open("playermatch.txt", "r+")
        rstring = pmfile.read()
        rstring = rstring[:-2]
        rstring = '['+rstring+']'
        rdict = yaml.safe_load(rstring)
        for i in rdict:
            if i['_id'] == matchid:
                fdict = i
        return(fdict)

    def multikey(self, heroname):
        matchidlist = []
        flag = 0
        playermatch = os.join.path("F:\\drev\\app\\files", "playermatch.txt")
        pmfile = open(playermatch, "r+")
        rstring = pmfile.read()
        rstring = rstring[:-2]
        rstring = '['+rstring+']'
        rdict = yaml.safe_load(rstring)
        for i in rdict:
            for key, values in i.items():
                if key == "heroname":
                    for j in values:
                        if j == heroname:
                            flag = 1
            if flag == 1:
                matchidlist.append(i['_id'])
            flag = 0
        print(matchidlist)
        hdict = {heroname: matchidlist}
        rhresult = json.dumps(hdict, indent=-1)
        playersecond = os.join.path("F:\\drev\\app\\files",
                                    "player_match_sec_hero.txt")
        secondarkey = open(playersecond, "a+")
        secondarkey.write(rhresult+'\n,\n')
        secondarkey.close()

    def deleterecord(self,matchid):
        playermatch = os.path.join("F:\\drev\\app\\files", "playermatch.txt")
        with open(playermatch, "r+") as file:
            rstring = file.read()
            rstring = rstring[:-2]
            rstring = '['+rstring+']'
            rdict = yaml.safe_load(rstring)
            for index, items in enumerate(rdict):
                if items['_id'] == matchid:
                    rdict.pop(index)

            result = json.dumps(rdict, indent=-1)
            result = result[2:-1]
            result = result + ","
            with open(playermatch, "w+") as file:
                file.write(result)
