import re
import yaml
import json
import time
import os

logfilepath="/home/vinay/fsproject/app"
filepath="/home/vinay/fsproject/app/files"

class regcl():

    def regfun():
        while(1):
            direct = os.path.join(logfilepath, "app.log")
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
            tlen = []
            midfile = os.path.join(filepath, "counterfile.txt")
            with open(midfile, "r+") as file:
                rstring = file.read()
                rdict = yaml.safe_load(rstring)
                for j in rdict:
                    for index, items in enumerate(mid):
                        if j['mid'] == items:
                            j['counter'] = j['counter'] + 1
                            mid.pop(index)
                            print(rdict)
                        else:
                            tdict = {"mid": items, "counter": 1}
                            tlen.append(tdict)
                            mid.pop(index)

            for index1, item1 in enumerate(tlen):
                for index2, item2 in enumerate(rdict):
                    if item1['mid'] == item2['mid']:
                        item1['counter'] = item1['counter'] + item2['counter']
                        rdict.pop(index2)

            tlen = tlen + rdict
            tc = 0
            for i in tlen:
                tc = tc + i['counter']
            for i in tlen:
                i['threshold'] = i['counter']/tc
            g = json.dumps(tlen, indent=-1)
            with open(midfile, "w+") as file:
                file.write(g)
            time.sleep(60)
