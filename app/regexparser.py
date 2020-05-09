import re
import yaml
import json
import time
import os
while(1):
    direct = r"E:\newprojj\Dota\app\app.log"
    matchlist = []
    regex = r'GET /midswid/(\d{10})'
    with open(direct, "r") as file:
        for line in file:
            for match in re.finditer(regex, line, re.S):
                match_text = match.group()
                matchlist.append(match_text)
    print(matchlist)
    mid = []
    for i in matchlist:
         k = i[-10:]
         mid.append(int(k))
    tlen = []
    print(mid)
    midfile = os.path.join("F:\\drev\\app\\files", "counterfile.txt")
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
                    print("in else")

    for index1, item1 in enumerate(tlen):
        for index2, item2 in enumerate(rdict):
            if item1['mid'] == item2['mid']:
                item1['counter'] = item1['counter'] + item2['counter']
                rdict.pop(index2)

    tlen = tlen + rdict
    print(tlen)
    g = json.dumps(tlen, indent=-1)
    print(tlen)
    g = g[1:-1]
    g = g+",\n"
    with open(midfile, "w+") as file:
        file.write(g)
    time.sleep(60)
