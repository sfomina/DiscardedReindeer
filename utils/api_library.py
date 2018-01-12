import json, requests, urllib2
import random
from requests.auth import HTTPBasicAuth
import dbLibrary



ibm_user = "867c9b88-87d2-4ebc-a055-70071421c0ba"
ibm_pass = "lb340eEJSNnM"



def create_profile(username, bio):
    headers = {'Content-Type' : 'text/plain;charset=utf-8'}
    link =  "https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13"
    data = bio
    #print json.dumps(personality_results, indent=1)

    personality_results = requests.post(link,headers=headers,data=data, auth=HTTPBasicAuth(ibm_user,ibm_pass))

    #now a dictionary
    personality_results = personality_results.json()

    #index big 5 emotions
    openn = personality_results["personality"][0]["percentile"]
    #print open
    
    consc = personality_results["personality"][1]["percentile"]
    #print consc
    
    extra =  personality_results["personality"][2]["percentile"]
    #print extra 
    
    agree =  personality_results["personality"][3]["percentile"]
    
    emot_range =  personality_results["personality"][4]["percentile"]
    
    #open database
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)

    #insert into personality table name and your scores
    dbLibrary.insertRow("personality" , ["username" , "open" , "consc" , "extra", "agree" , "emotRange"] , [username, openn , consc , extra , agree, emot_range], cursor)
    
    #close database
    dbLibrary.commit(db)
    dbLibrary.closeFile(db)
    
    

#returns name of potential match or 0 if no potential matches
def find_match(username, prefGender,gender):
    db = dbLibrary.openDb("../dating.db")
    cursor = dbLibrary.createCursor(db)

    my_open = cursor.execute("SELECT open FROM personality WHERE username = '" + username + "';")
    my_consc = cursor.execute("SELECT consc FROM personality WHERE username = '" + username + "';")
    my_extra = cursor.execute("SELECT extra FROM personality WHERE username = '" + username + "';")
    my_agree = cursor.execute("SELECT agree FROM personality WHERE username = '" + username + "';")
    my_emot_range = cursor.execute("SELECT emotRange FROM personality WHERE username = '" + username + "';")
    my_total = my_open + my_consc + my_extra + my_agree + my_emot_range
    
    #select all the names where prefGender = their gender and their prefgender = my gender
    pos_matches_cursor = cursor.execute("SELECT username FROM users WHERE prefGender = '" + gender + "' and gender = '" + prefGender + "';")

    pos_matches = []
    for item in pos_matches_cursor:
        for match in item:
            pos_matches.append(match)
    

    
    for user in pos_matches:
        openn =  cursor.execute("SELECT open FROM personality WHERE username = '" + user + "';")
        consc = cursor.execute("SELECT consc FROM personality WHERE username = '" + user + "';")
        extra = cursor.execute("SELECT extra FROM personality WHERE username = '" + user + "';")
        agree = cursor.execute("SELECT agree FROM personality WHERE username = '" + user + "';")
        emot_range = cursor.execute("SELECT emotRange FROM personality WHERE username = '" + user + "';")

        #differences
        od = abs(openn - my_open)
        cd = abs(consc - my_consc)
        ed = abs(extra - my_extra)
        ad = abs(agree - my_agree)
        emd = abs(emot_range - my_emot_range)
        total = od + cd + ed + ad + emd
        
        percent_similarity = 100 - ((total/my_total) * 100)

        #field posMatch
        if percent_similarity >= 60:
            update ("users" , "posMatch" , "'" + user + "'", "username = '" + username + "'")
            dbLibrary.commit(db)
            dbLibrary.closeFile(db)
            return user
    dbLibrary.closeFile(db)
    return 0
            
        
    
   
    
    #personality
    # name|openness | conscientiousness | extraversion | agreeableness | emotional range
    #select each of these


    




