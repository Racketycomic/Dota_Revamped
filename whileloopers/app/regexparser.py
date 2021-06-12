import re
import yaml
import json
import time
import os
from collections import Counter

filepath = "/home/vinay/fsproject2/app/files"
logpath ="/home/vinay/fsproject2/app"
class regcl():

    def regfun(self):
            print("In regexparser")
            flag=0
            direct = os.path.join(logpath, "app.log")
            direct2 = os.path.join(filepath, "playermatch_index.txt")
            matchlist = []
            regex = r'GET /midswid/(\d{10})'
            with open(direct, "r") as file:
                for line in file:
                    for match in re.finditer(regex, line, re.S):
                        match_text = match.group()
                        matchlist.append(match_text)
            mid = []
            for i in matchlist:
                 k = i[-10:]
                 mid.append(int(k))
            mid = dict(Counter(mid))
            tdict =[]
            for key,values in mid.items():
                tdict.append({"mid":key,"counter":values})
            print(tdict)
            midfile = os.path.join(filepath, "counterfile.txt")
            with open(midfile, "r+") as file:
                rstring = file.read()
                rdict = yaml.safe_load(rstring)

            if rdict is not None:
                for index1, item1 in enumerate(rdict):
                    for index2, item2 in enumerate(tdict):
                        if item1['mid'] == item2['mid']:
                            item1['counter'] = item1['counter'] + item2['counter']
                            tdict.pop(index2)


            if rdict is None:
                tc = 0
                for i in tdict:
                    tc = tc + i['counter']
                for i in tdict:
                    i['threshold'] = i['counter']/tc
                g = json.dumps(tdict, indent=-1)
                with open(midfile, "w+") as file:
                    file.write(g)
                flag = 1
            else:
                rdict = rdict + tdict
                print(rdict)
                tc = 0
                for i in rdict:
                    tc = tc + i['counter']
                for i in rdict:
                    i['threshold'] = i['counter']/tc
                print(rdict)
                g = json.dumps(rdict, indent=-1)
                with open(midfile, "w+") as file:
                    file.write(g)

            with open(direct2, "r+") as file:
                rstring = file.read()
                rstring = rstring[:-2]
                rstring = '[' + rstring + ']'
                rlist = yaml.safe_load(rstring)
            print(rlist)
            if not flag:
                kstring = ""
                for index1, item1 in enumerate(rdict):
                    for index2, item2 in enumerate(rlist):
                        if item1['mid'] == item2['matchid']:
                            item2['threshold'] = item1['threshold']
                with open(direct2, "w+") as file:
                    for i in rlist:
                        rstring = json.dumps(i, indent=-1)
                        kstring = rstring+"\n,\n"
                    file.write(kstring)
