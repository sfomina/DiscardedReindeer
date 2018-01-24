import json, requests, urllib2
import random
from requests.auth import HTTPBasicAuth
import dbLibrary



ibm_user = "867c9b88-87d2-4ebc-a055-70071421c0ba"
ibm_pass = "lb340eEJSNnM"


#============================CREATE PROFILE ====================================================
def create_profile(username, bio):
    headers = {'Content-Type' : 'text/plain;charset=utf-8'}
    link =  "https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13"
    data = bio
    #print json.dumps(personality_results, indent=1)

    personality_results = requests.post(link,headers=headers,data=data, auth=HTTPBasicAuth(ibm_user,ibm_pass))

    #now a dictionary
    personality_results = personality_results.json()

    #print personality_results
    #index big 5 emotions
    openn = personality_results["personality"][0]["percentile"]
    consc = personality_results["personality"][1]["percentile"]
    extra =  personality_results["personality"][2]["percentile"]
    agree =  personality_results["personality"][3]["percentile"]
    emot_range =  personality_results["personality"][4]["percentile"]

    #index needs
    challenge = personality_results["needs"][0]["percentile"]
    closeness = personality_results["needs"][1]["percentile"]
    curiosity = personality_results["needs"][2]["percentile"]
    excitement = personality_results["needs"][3]["percentile"]
    harmony = personality_results["needs"][4]["percentile"]
    ideal = personality_results["needs"][5]["percentile"]
    liberty = personality_results["needs"][6]["percentile"]
    love = personality_results["needs"][7]["percentile"]
    practicality = personality_results["needs"][8]["percentile"]
    expression = personality_results["needs"][9]["percentile"]
    stability = personality_results["needs"][10]["percentile"]
    structure = personality_results["needs"][11]["percentile"]

    #open database
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)

    #insert into personality table name and your scores
    dbLibrary.insertRow("personality" , ["username" , "open" , "consc" , "extra", "agree" , "emotRange", "challenge" ,"closeness", "curiosity", "excitement", "harmony", "ideal", "liberty", "love", "practicality" , "expression", "stability", "structure"] , [username, openn , consc , extra , agree, emot_range, challenge, closeness, curiosity, excitement, harmony, ideal, liberty, love, practicality, expression, stability, structure], cursor)

    #close database
    dbLibrary.commit(db)
    dbLibrary.closeFile(db)
#==================================================================================================================

#===================================GET CS SCORE===================================================================
def cs_score (username, pos_match, cursor):
    my_lang = cursor.execute("SELECT lang FROM users WHERE username = '" + username + "';")
    lang =  cursor.execute("SELECT lang FROM users WHERE username = '" + pos_match + "';")
    my_sortAlg =  cursor.execute("SELECT sortAlg FROM users WHERE username = '" + username + "';")
    sortAlg =  cursor.execute("SELECT sortAlg FROM users WHERE username = '" + pos_match + "';")
    my_type =  cursor.execute("SELECT type FROM users WHERE username = '" + username + "';")
    typee =  cursor.execute("SELECT type FROM users WHERE username = '" + pos_match + "';")
    my_bitcoin =  cursor.execute("SELECT bitcoin FROM users WHERE username = '" + username + "';")
    bitcoin =  cursor.execute("SELECT bitcoin FROM users WHERE username = '" + pos_match + "';")
    my_nameCase =  cursor.execute("SELECT nameCase FROM users WHERE username = '" + username + "';")
    nameCase =  cursor.execute("SELECT nameCase FROM users WHERE username = '" + pos_match + "';")
    my_braces =  cursor.execute("SELECT braces FROM users WHERE username = '" + username + "';")
    braces =  cursor.execute("SELECT braces FROM users WHERE username = '" + pos_match + "';")

    total = 0
    if my_lang == lang:
        total += 1
    if my_sortAlg == sortAlg:
        total += 1
    if my_type == typee :
        total +=1
    if my_bitcoin == bitcoin:
        total+=1
    if my_nameCase == nameCase:
        total += 1
    if my_braces == braces:
        total +=1

    percent = total/6
    return percent



#==================================================================================================================

#=================================FIND MATCH ========================================================================


#returns name of potential match or "none" if no potential matches
#stores in users table:  name of current suggested match, percent similarity,and differences for each trait for later use in learning
def find_match(username):
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)

    queue = cursor.execute("SELECT queue FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    queue = queue.split("-")
    for i in range(len(queue)):
        queue[i] = queue[i].split(",")

    #if someone already matched with you
    if len(queue) > 1:
        match = queue[1][0]
        dbLibrary.update ("users" , "posMatch" , "'" + match + "'", "username = '" + username + "'", cursor)

        dbLibrary.update("users" , "csPercent", queue[1][2] , "username = '" + username + "'" , cursor)

        dbLibrary.update("users", "percent" ,queue[1][1], "username = '" + username + "'", cursor)

        differences = ["od" , "cd" , "ed" , "ad" , "emd" , "challd" , "curd" , "exd" , "hd" , "ideald" , "libd" , "lod" , "pd", "exprd" , "stabd", "strucd"]
        var_diff = [float(queue[1][3]) ,float(queue[1][4]) ,float(queue[1][5]) ,float(queue[1][6]) ,float(queue[1][7]) ,float(queue[1][8]) , float(queue[1][9]),float(queue[1][10]) ,float(queue[1][11]) ,float(queue[1][12]) , float(queue[1][13]) ,float(queue[1][14]) , float(queue[1][15]) ,float(queue[1][16]) ,float(queue[1][17]) ,float(queue[1][18])]

        for p in range(16):
            dbLibrary.update("users", differences[p] , var_diff[p], "username = '" + username + "'", cursor)

        queue.pop(1)
        for n in range(len(queue)):
            queue[n] = ",".join(queue[n])
        queue = "-".join(queue)
        dbLibrary.update("users", "queue" , "'" + queue + "'" ,"username = '" + username + "'", cursor)
        dbLibrary.commit(db)
        dbLibrary.closeFile(db)
        return match


    prefGender = cursor.execute("SELECT prefGender FROM users WHERE username = '" + username + "';").fetchall()[0][0]

    gender = cursor.execute("SELECT gender FROM users WHERE username =  '" + username + "';").fetchall()[0][0]

    my_age = cursor.execute("SELECT age FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    upper_bound = my_age + 15
    lower_bound = my_age - 15

    #selecting each of my subscores
    my_open = cursor.execute("SELECT open FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_consc = cursor.execute("SELECT consc FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_extra = cursor.execute("SELECT extra FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_agree = cursor.execute("SELECT agree FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_emot_range = cursor.execute("SELECT emotRange FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_challenge = cursor.execute("SELECT challenge FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_curiosity = cursor.execute("SELECT curiosity FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_excitement = cursor.execute("SELECT excitement FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_harmony = cursor.execute("SELECT harmony FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_ideal = cursor.execute("SELECT ideal FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_liberty = cursor.execute("SELECT liberty FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_love = cursor.execute("SELECT love FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_practicality = cursor.execute("SELECT practicality FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_expression = cursor.execute("SELECT expression FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_stability = cursor.execute("SELECT stability FROM personality WHERE username = '" + username + "';").fetchall()[0][0]
    my_structure = cursor.execute("SELECT structure FROM personality WHERE username = '" + username + "';").fetchall()[0][0]

    #select MY coefficients from formula table
    my_oco = cursor.execute("SELECT openCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_cco =  cursor.execute("SELECT conscCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_eco =  cursor.execute("SELECT extraCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_aco =  cursor.execute("SELECT agreeCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_emotco =  cursor.execute("SELECT emotRangeCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_challco =  cursor.execute("SELECT challengeCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_curco =  cursor.execute("SELECT curiosityCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_exco =  cursor.execute("SELECT excitementCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_hco =  cursor.execute("SELECT harmonyCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_idealco =  cursor.execute("SELECT idealCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_libco =  cursor.execute("SELECT libertyCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_loco =  cursor.execute("SELECT loveCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_pco =  cursor.execute("SELECT practicalityCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_exprco =  cursor.execute("SELECT expressionCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_stabco =  cursor.execute("SELECT stabilityCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_strucco =  cursor.execute("SELECT structureCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
    my_denominator = my_oco + my_cco + my_eco + my_aco + my_emotco + my_challco + my_curco + my_exco + my_hco + my_idealco + my_libco + my_loco+ my_pco+ my_exprco + my_stabco + my_strucco

    my_csco =  cursor.execute("SELECT csCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]

    my_suggested_users = cursor.execute("SELECT suggested FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_suggested_list = my_suggested_users.split(",")


    #filter out by gender and age and not me
    pos_matches_cursor = cursor.execute("SELECT username FROM users WHERE prefGender = '" + gender + "' and gender = '" + prefGender + "' and username != '" + username + "' and (age <= " + str(upper_bound) + " or age >= " + str(lower_bound)  + ");").fetchall()

    pos_matches = []
    for item in pos_matches_cursor:
        for match in item:
            pos_matches.append(str(match))



    for user in pos_matches:
        if user not in my_suggested_list:
            openn =  cursor.execute("SELECT open FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            consc = cursor.execute("SELECT consc FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            extra = cursor.execute("SELECT extra FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            agree = cursor.execute("SELECT agree FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            emot_range = cursor.execute("SELECT emotRange FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            challenge = cursor.execute("SELECT challenge FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            curiosity = cursor.execute("SELECT curiosity FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            excitement = cursor.execute("SELECT excitement FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            harmony = cursor.execute("SELECT harmony FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            ideal = cursor.execute("SELECT ideal FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            liberty = cursor.execute("SELECT liberty FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            love = cursor.execute("SELECT love FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            practicality = cursor.execute("SELECT practicality FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            expression = cursor.execute("SELECT expression FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            stability = cursor.execute("SELECT stability FROM personality WHERE username = '" + user + "';").fetchall()[0][0]
            structure = cursor.execute("SELECT structure FROM personality WHERE username = '" + user + "';").fetchall()[0][0]

            #select coefficients from formula table
            oco = cursor.execute("SELECT openCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            cco =  cursor.execute("SELECT conscCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            eco =  cursor.execute("SELECT extraCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            aco =  cursor.execute("SELECT agreeCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            emotco =  cursor.execute("SELECT emotRangeCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            challco =  cursor.execute("SELECT challengeCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            curco =  cursor.execute("SELECT curiosityCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            exco =  cursor.execute("SELECT excitementCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            hco =  cursor.execute("SELECT harmonyCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            idealco =  cursor.execute("SELECT idealCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            libco =  cursor.execute("SELECT libertyCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            loco =  cursor.execute("SELECT loveCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            pco =  cursor.execute("SELECT practicalityCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            exprco =  cursor.execute("SELECT expressionCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            stabco =  cursor.execute("SELECT stabilityCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            strucco =  cursor.execute("SELECT structureCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]
            denominator = oco + cco + eco + aco + emotco + challco + curco + exco + hco + idealco + libco + loco+ pco+ exprco + stabco + strucco

            csco =  cursor.execute("SELECT csCo FROM formula WHERE username = '" + user + "';").fetchall()[0][0]

            #differences
            od = abs(openn - my_open)
            cd = abs(consc - my_consc)
            ed = abs(extra - my_extra)
            ad = abs(agree - my_agree)
            emd = abs(emot_range - my_emot_range)
            challd = abs(challenge - my_challenge)
            curd = abs(curiosity - my_curiosity)
            exd = abs(excitement - my_excitement)
            hd = abs(harmony - my_harmony)
            ideald = abs(ideal - my_ideal)
            libd = abs(liberty - my_liberty)
            lod = abs(love - my_love)
            pd = abs(practicality - my_practicality)
            exprd = abs(expression - my_expression)
            stabd = abs(stability - my_stability)
            strucd = abs(structure - my_structure)

            total = oco*od + cco*cd + eco*ed + aco*ad + emotco*emd + challco*challd + curco*curd + exco*exd + hco*hd + idealco*ideald + libco*libd + loco*lod + pco*pd + exprco*exprd + stabco*stabd + strucco*strucd
            my_total = my_oco*od + my_cco*cd + my_eco*ed + my_aco*ad + my_emotco*emd + my_challco*challd + my_curco*curd + my_exco*exd + my_hco*hd + my_idealco*ideald + my_libco*libd + my_loco*lod + my_pco*pd + my_exprco*exprd + my_stabco*stabd + my_strucco*strucd

            #IF YOU SWIPED LEFT ON A PERSON
            #lowest difference must be weighted less
            #highest difference must be weighted more

            percent_similarity = 1- (total/denominator)
            my_percent_similarity = 1 - (my_total/my_denominator)


            cs_percent = cs_score(username , user , cursor)

            percent_similarity = (percent_similarity + csco * cs_percent)/ (1 + csco)
            my_percent_similarity = (my_percent_similarity + my_csco *cs_percent)/ (1 + my_csco)

            overall_percent_similarity = 100* ((percent_similarity * my_percent_similarity)**(0.5))

            #field posMatch
            if overall_percent_similarity >= 60:
                dbLibrary.update ("users" , "posMatch" , "'" + user + "'", "username = '" + username + "'", cursor)
                dbLibrary.update("users" , "csPercent", str(cs_percent) , "username = '" + username + "'" , cursor)
                my_suggested_list.append(user)
                my_suggested_users = ",".join(my_suggested_list)

                #updating your match's suggested list
                suggested_users = cursor.execute("SELECT suggested FROM users WHERE username = '" + user + "';").fetchall()[0][0]
                suggested_list = suggested_users.split(",")
                suggested_list.append(username)
                suggested_users = ",".join(suggested_list)
                dbLibrary.update("users" , "suggested", "'" + suggested_users + "'","username = '" + user + "'", cursor )


                dbLibrary.update("users" , "suggested", "'" + my_suggested_users + "'","username = '" + username + "'", cursor )

                dbLibrary.update("users", "percent" , str(int(overall_percent_similarity)), "username = '" + username + "'", cursor)

                differences = ["od" , "cd" , "ed" , "ad" , "emd" , "challd" , "curd" , "exd" , "hd" , "ideald" , "libd" , "lod" , "pd", "exprd" , "stabd", "strucd"]
                var_diff = [od , cd , ed , ad , emd , challd , curd, exd , hd , ideald , libd , lod , pd , exprd , stabd , strucd]
                for i in range(16):
                    dbLibrary.update("users", differences[i] , var_diff[i], "username = '" + username + "'", cursor)

                #adding you to your match's queue
                queue = cursor.execute("SELECT queue FROM users WHERE username = '" + user + "';").fetchall()[0][0]
                queue = queue.split("-")
                for i in range(len(queue)):
                    queue[i] = queue[i].split(",")
                queue.append([username, str(int(overall_percent_similarity)), str(cs_percent), str(od) ,str(cd), str(ed) , str(ad) , str(emd) , str(challd) , str(curd), str(exd) , str(hd) , str(ideald) , str(libd) , str(lod) , str(pd) , str(exprd) , str(stabd) , str(strucd)])
                for n in range(len(queue)):
                    queue[n] = ",".join(queue[n])
                queue = "-".join(queue)
                dbLibrary.update("users", "queue" , "'" + queue + "'" ,"username = '" + user + "'", cursor)


                dbLibrary.commit(db)
                dbLibrary.closeFile(db)
                return user


    dbLibrary.update ("users" , "posMatch" , "'none'", "username = '" + username + "'", cursor)
    dbLibrary.commit(db)
    dbLibrary.closeFile(db)
    return "none"

#===================================================================================================

#===============================ADJUST FORMULA======================================================
#updates formula table coefficients
#should be called if user didn't like suggested match
def adjust_formula(username):
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)

    #selecting each of my differences
    my_od = cursor.execute("SELECT od FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_cd = cursor.execute("SELECT cd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_ed = cursor.execute("SELECT ed FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_ad = cursor.execute("SELECT ad FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_emd = cursor.execute("SELECT emd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_challd = cursor.execute("SELECT challd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_curd = cursor.execute("SELECT curd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_exd = cursor.execute("SELECT exd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_hd = cursor.execute("SELECT hd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_ideald = cursor.execute("SELECT ideald FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_libd = cursor.execute("SELECT libd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_lod = cursor.execute("SELECT lod FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_pd = cursor.execute("SELECT pd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_exprd = cursor.execute("SELECT exprd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_stabd = cursor.execute("SELECT stabd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_strucd = cursor.execute("SELECT strucd FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    my_csPercent = cursor.execute("SELECT csPercent FROM users WHERE username = '" + username + "';").fetchall()[0][0]

    differences = [my_od, my_cd, my_ed, my_ad, my_emd, my_challd, my_curd, my_exd, my_hd, my_ideald, my_libd, my_lod, my_pd, my_exprd, my_stabd, my_strucd]
    coefs = ["openCo", "conscCo","extraCo","agreeCo","emotRangeCo","challengeCo","curiosityCo","excitementCo", "harmonyCo","idealCo","libertyCo","loveCo", "practicalityCo", "expressionCo","stabilityCo","structureCo"]

    my_csco =  cursor.execute("SELECT csCo FROM formula WHERE username = '" + username + "';").fetchall()[0][0]

    #adjust cs coefficient if necessary
    if my_csPercent < 0.4:
        my_csco += 0.05

    #find the highest difference
    maxIndex  = 0
    for i in range(len(differences)):
        if differences[i] > differences[maxIndex]:
            maxIndex = i


    highest = differences[maxIndex]
    if highest > 0.3:
       coeff = cursor.execute("SELECT " + coefs[maxIndex] + " FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
       coeff += 0.25
       dbLibrary.update("formula", coefs[maxIndex], str(coeff), "username = '" + username + "'", cursor)

    else:
        #find the lowest difference
        minIndex = 0
        for i in range(len(differences)):
            if differences[i] < differences[minIndex]:
                minIndex = i
        lowest = differences[minIndex]
        coeff = cursor.execute("SELECT " + coefs[minIndex] + " FROM formula WHERE username = '" + username + "';").fetchall()[0][0]
        coeff += 0.25
        dbLibrary.update("formula", coefs[minIndex], str(coeff), "username = '" + username + "'", cursor)

    dbLibrary.commit(db)
    dbLibrary.closeFile(db)

#==========================================================================================

#=============================LIKING A SUGGESTED MATCH====================================================

#adds someone in your liked field, and checks to see if should add anything to secured field
def like(username, liked_match):
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)
    liked_str = cursor.execute("SELECT liked FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    liked_list = liked_str.split(",")

    secured_str = cursor.execute("SELECT secured FROM users WHERE username = '" + username + "';").fetchall()[0][0]
    secured_list = secured_str.split(",")

    their_secured_str = cursor.execute("SELECT secured FROM users WHERE username = '" + liked_match + "';").fetchall()[0][0]
    their_secured_list = their_secured_str.split(",")

    liked_list.append(liked_match)

    their_liked_str = cursor.execute("SELECT liked FROM users WHERE username = '" + liked_match + "';").fetchall()[0][0]
    their_liked_list = their_liked_str.split(",")
    if username in their_liked_list:
        secured_list.append(liked_match)
        their_secured_list.append(username)
        secured_str = ",".join(secured_list)
        their_secured_str = ",".join(their_secured_list)
        dbLibrary.update("users" , "secured", "'" + secured_str + "'","username = '" + username + "'", cursor )
        dbLibrary.update("users" , "secured", "'" + their_secured_str + "'","username = '" + liked_match + "'", cursor )


    liked_str = ",".join(liked_list)
    dbLibrary.update("users" , "liked", "'" + liked_str + "'","username = '" + username + "'", cursor )

    dbLibrary.commit(db)
    dbLibrary.closeFile(db)
