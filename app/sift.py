from app import dbservices as db
import requests
import collections
import random


class playertable():

    def getinfo(self, playerid):

        plist = []
        plist.append(playerid)
        req1 = requests.get(f'https://api.opendota.com/api/players/{playerid}/wl')
        json1 = req1.json()
        for key,value in json1.items():
            plist.append(value)
        plist.append(int(plist[1]+plist[2]))
        req2 = requests.get(f"https://api.opendota.com/api/players/{playerid}/totals")
        json2 = req2.json()

        #gpm calc
        for i in json2:
            if i['field'] == 'gold_per_min':
                mydict=i
                break

        l1 = []
        for key, values in mydict.items():
            l1.append(values)
        gpm = l1[2]/l1[1]
        plist.append(int(gpm))

        #xpm calc
        for i in json2:
            if i['field'] == 'xp_per_min':
                mydict = i
                break
        l1 = []
        for key, values in mydict.items():
            l1.append(values)

        xpm = l1[2]/l1[1]
        plist.append(int(xpm))   #[id,win,loss,totalmatches,gpm,xpm]

        #kda calc
        for i in json2:
            if i['field'] == 'kda':
                mydict = i
                break

        l1 = []
        for key, values in mydict.items():
            l1.append(values)

        kda = l1[2]/l1[1]
        plist.append(kda)  #[id,win,loss,totalmatches,gpm,xpm,kda]

        req3 = requests.get(f"https://api.opendota.com/api/players/{playerid}")
        json3 = req3.json()
        for key, values in json3.items():
            if key == "solo_competitive_rank":
                plist.append(values)           #[id,win,loss,totalmatches,gpm,xpm,kda,mmr]

        db.player.insert_one({"_id": plist[0], "no_wins": plist[1], "no_losses": plist[2],
                          "no_match": plist[3], "avg_gpm": plist[4], "avg_xpm":plist[5],
                          "avg_kda": plist[6], "mmr": plist[7]}
                          )

        ####!!!!!!!!!!!player Performance table !!!!!!!!!!!!!#

        re1 = requests.get(f'https://api.opendota.com/api/players/{playerid}/rankings')
        j1 = re1.json()
        print(j1)
        id = [d['hero_id'] for d in j1]
        perc = [d['percent_rank'] for d in j1]
        size = len(id)
        print(size)

        playerdict = dict(zip(id, perc))
        print(playerdict)
        odpd = collections.OrderedDict(sorted(playerdict.items()))
        print(odpd)

        perc1 = list(odpd.values())
        print(perc1)
        id1 = list(odpd.keys())
        print(id1)
        print(len(id1))
        k = 0
        result = 0
        score = 0
        desc = []
        while k<size:
            result=perc1[k]
            print(result)
            if result <= 0.2:
                desc.append("Herald")

            elif result >0.2 and result<=  0.3:
                desc.append("Guardian")

            elif result >0.3 and result <= 0.4:
                desc.append("Crusader")

            elif result >0.4 and result<=0.5:
                desc.append("Archon")

            elif result >0.5 and result<=0.7:
                desc.append("Legend")

            elif result>0.7 and result<=0.8:
                desc.append("Ancient")

            elif result >0.8 and result <=0.9:
                desc.append("Divine")

            else:
                desc.append("Immortal")

            k = k+1


        print(desc)
        names=[]
        k=0
        while k<size:
            nam = db.herodetails.find_one({"_id": id1[k]}, {"_id": 0, "hero_name": 1})
            for key,values in nam.items():
                names.append(values)
            k=k+1


        print(names)


        db.playerhero.insert_one({"hid": id1, "score": perc1, "_id": playerid,
                               "performance": desc, "heroname": names}
                             )


class matchtable():

    def getmatch(self, matchid):

        re5=requests.get(f"https://api.opendota.com/api/matches/{matchid}")
        js5=re5.json()


        list5=[]
        for key,values in js5.items():
            if key=="players":
                list5.append(values)

        print(list5)
        death=[]
        for i in list5:
            for j in i:

                for key, values in j.items():
                    if key == "deaths":
                        death.append(values)
        sumd=sum(death)
        print(sumd)
        assist=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="assists":
                        assist.append(values)

        suma=sum(assist)
        print(suma)
        kills=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="kills":
                        kills.append(values)

        sumk=sum(kills)
        print(sumk)




        [d[0] for d in list5]

        #total gold

        tot_gold=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="total_gold":
                        tot_gold.append(values)




        print(tot_gold)
        sumg=sum(tot_gold)


        tot_xp=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="total_xp":
                        tot_xp.append(values)

        sumx=sum(tot_xp)

        for key,values in js5.items():
            if key=="duration":
                duration=round(values/60)

        print(duration)

        for key,values in js5.items():
            if key=="radiant_win":
                if values:
                    winner="Radiant"
                else:
                    winner="Dire"

        print(winner)

        db.match.insert_one({"_id": matchid, "tot_kills": sumk,
                       "tot_assist": suma, "tot_death": sumd ,
                         "tot_gold": sumg, "tot_xp": sumx,
                         "duration": duration, "winner": winner}
                         )


        ############!!!!!!!!!!!!PLAYER_MATCH TABLE !!!!!!!!!!!!!!!!!!!!##############
        kda=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="kda":
                        kda.append(values)

        print(kda)

        gpm=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key == "gold_per_min":
                        gpm.append(values)

        print(gpm)

        xpm=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="xp_per_min":
                        xpm.append(values)


        print(xpm)

        print(list5)
        playernames=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if  "personaname" not in j.keys():
                        playernames.append("Anonymous")
                        break
                    if key == "personaname":
                        playernames.append(values)


        print(playernames)


        playerids=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="account_id":
                        if values==None:
                            randkey=random.randrange(1000,9999,20)
                            playerids.append(randkey)
                        else:
                            playerids.append(values)


        print(playerids)

        heroids=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="hero_id":
                        heroids.append(values)

        print(heroids)

        heronames=[]
        k=0
        while k<10:
            heroes = db.herodetails.find_one({"_id": heroids[k]}, {"hero_name": 1, "_id": 0})
            for key, values in heroes.items():
                heronames.append(values)
            k = k+1

        print(heronames)
        radstat=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="isRadiant":
                        radstat.append(values)


        print(radstat)
        teamstat=[]
        for i in radstat:
            if i:
                teamstat.append("Radiant")
            else:
                teamstat.append("Dire")
        print(teamstat)


        winstatus=[]
        for i in list5:
            for j in i:
                for key,values in j.items():
                    if key=="win":
                        winstatus.append(values)
        print(winstatus)

        actwinstat=[]
        for i in winstatus:
            if i:
                actwinstat.append("WON")
            else:
                actwinstat.append("LOST")

        print(actwinstat)


        db.playermatch.insert_one({"_id": matchid, "playerid": playerids,
                                "kill_count": kills, "death_count": death,
                                "assist_count": assist, "kdaratio": kda,
                                "playername": playernames, "xpm": xpm,
                                "gpm": gpm, "team": teamstat,
                                "result": actwinstat, "heroname": heronames}
                               )


        ########!!!!!!!!!!!!!!! ANA TABLE !!!!!!!!!!!!!! #########
        #re1=requests.get("https://api.opendota.com/api/players/311360822/rankings")
        #js1=re1.json()
        #id=[d['hero_id'] for d in js1]
        #perc=[d['percent_rank'] for d in js1]
        #prodict=dict(zip(id,perc))
        #print(prodict)
        #odpd=collections.OrderedDict(sorted(prodict.items()))
        #print(odpd)
        #k=0
        #for key,values in odpd.items():
            #user=ana(hero_id=key,score=values)
            #db.session.add(user)
            #db.session.commit()
            #k=k+1



        #!!!!!!!!!!!Hero TABle !!!!!!!!!!!#
        #def getheroinfo(self):
        #idar=[]
        #total=[]
        #names=[]
        #wins=[]
        #loss=[]
        #l1=[]
        #l2=[]

        #req1=requests.get("https://api.opendota.com/api/heroes")
        #json1=req1.json()
        #print(json1)

        #for i in json1:
        #    if i['id']:
        #        idar.append(i['id'])

        #for i in json1:
        #    if i['localized_name']:
        #        names.append(i['localized_name'])

        #print(names[0])
        #print(len(names))
        #print(len(idar))
    #    print(idar)
#
#        k=110
#        while k < 140:
#            req2=requests.get(f"https://api.opendota.com/api/heroes/{k}/durations")
#            json2=req2.json()
#            print(k)

#            if(len(json2) == 0):
#                k = k+1
#                continue

#            for i in json2:
#                if i["games_played"]:
#                    l1.append(i['games_played'])
#            tots=sum(l1)
#            total.append(tots)
#            for i in json2:
#                if i['wins']:
#                    l2.append(i['wins'])
#            w=sum(l2)
#            wins.append(w)
#            l=tots-w
#            loss.append(l)
#            k=k+1



#        print(len(total))
#
#        print(k)


#        m=0
        #while m < 119:
            #herodetails.insert_one({"hero_name": names[m], "_id": idar[m],
                                ##    "tot_match": total[m], "wins": wins[m],
                                #    "loss": loss[m]
                                #    }
                                 # )
            #m=m+1
            #user=hero(hero_name=names[m],hid=idar[m],tot_match=total[m],wins=wins[m],loss=loss[m])
            #db.session.add(user)
            #db.session.commit()
            #m=m+1
