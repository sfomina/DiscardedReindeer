import sqlite3, hashlib   #enable control of an sqlite database

f="dating.db"

def encrypt_password(password):
    encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
    #print encrypted_pass
    return encrypted_pass

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
db.create_function('encrypt', 1, encrypt_password)
c = db.cursor()    #facilitate db ops

create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL, name TEXT NOT NULL, age INTEGER NOT NULL,gender TEXT NOT NULL, prefGender TEXT NOT NULL, lang TEXT NOT NULL, sortAlg TEXT NOT NULL, type TEXT NOT NULL, bitcoin TEXT NOT NULL, nameCase TEXT NOT NULL, braces TEXT NOT NULL, bio TEXT NOT NULL, img_name TEXT NOT NULL, posMatch TEXT, percent INTEGER, od DECIMAL, cd DECIMAL, ed DECIMAL, ad DECIMAL, emd DECIMAL, challd DECIMAL, curd DECIMAL, exd DECIMAL, hd DECIMAL, ideald DECIMAL, libd DECIMAL, lod DECIMAL, pd DECIMAL, exprD DECIMAL, stabd DECIMAL, strucd DECIMAL, csPercent DECIMAL, suggested TEXT, queue TEXT );"



create_personality = "CREATE TABLE personality (username TEXT PRIMARY KEY, open DECIMAL NOT NULL, consc DECIMAL, extra DECIMAL, agree DECIMAL, emotRange DECIMAL, challenge DECIMAL, closeness DECIMAL, curiosity DECIMAL, excitement DECIMAL, harmony DECIMAL, ideal DECIMAL, liberty DECIMAL, love DECIMAL, practicality DECIMAL, expression DECIMAL, stability DECIMAL, structure DECIMAL);"

#table of coefficients
create_formula = "CREATE TABLE formula (username TEXT PRIMARY KEY,openCo DECIMAL, conscCo DECIMAl, extraCo DECIMAL, agreeCo DECIMAL, emotRangeCo DECIMAL, challengeCo DECIMAL, curiosityCo DECIMAL, excitementCo DECIMAL, harmonyCo DECIMAL, idealCo DECIMAL, libertyCo DECIMAL, loveCo DECIMAL, practicalityCo DECIMAL, expressionCo DECIMAL, stabilityCo DECIMAL, structureCo DECIMAL, csCo DECIMAL)"



#create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);"
insert_admin = "INSERT INTO users VALUES ('test', encrypt('test'), 'test', '18', 'Male', 'Male', 'Java', 'Merge Sort', 'OOP', 'No', 'snake_case', 'First', 'blah blah bio');"

#create formula table

insert_admin = "INSERT INTO users VALUES ('test', encrypt('test'));"

try:
    c.execute(create_users)
    c.execute(create_personality)
    c.execute(create_formula)
    #c.execute(insert_admin)

except:
    pass

db.commit() #save changes
#db.close()  #close database
