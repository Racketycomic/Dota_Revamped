import time
import os
import yaml
import json

filepath ="/home/vinay/fsproject2/app/files"
class delmain():
    
    counfile = os.path.join(filepath, "counterfile.txt")
    midfile = os.path.join(filepath, "playermatch.txt")
    indfile = os.path.join(filepath, "playermatch_index.txt")
    with open(counfile, "r+") as file:
        rstring = file.read()
        rdict = yaml.safe_load(rstring)
        least = 10
        if len(rdict) > 4:
            for i in rdict:
                if i['threshold'] < least:
                    print(i['threshold'])
                    least = i['threshold']
                    bootid = i['mid']
    with open(midfile, "r+") as file:
        rstring = file.read()
        rstring = rstring[:-2]
        rstring = '['+rstring+']'
        rlist = yaml.safe_load(rstring)
        for i in rlist:
            if i['matchid'] == bootid:
                i['matchid'] = "*"
    with open(midfile, "w+") as file:
        rstring = json.dumps(rlist, indent=-1)
        file.write(rstring)
