import sqlite3, hashlib   #enable control of an sqlite database

f="dating.db"

def encrypt_password(password):
    encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
    #print encrypted_pass
    return encrypted_pass

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
db.create_function('encrypt', 1, encrypt_password)
c = db.cursor()    #facilitate db ops

create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL, name TEXT NOT NULL, age INTEGER NOT NULL, gender TEXT NOT NULL, prefGender TEXT NOT NULL, lang TEXT NOT NULL, sortAlg TEXT NOT NULL, type TEXT NOT NULL, bitcoin TEXT NOT NULL, nameCase TEXT NOT NULL, braces TEXT NOT NULL, bio TEXT NOT NULL);"

create_personality = "CREATE TABLE personality (username TEXT PRIMARY KEY, open DECIMAL NOT NULL, consc DECIMAL NOT NULL, extra DECIMAL NOT NULL, agree DECIMAL NOT NULL, emotRange DECIMAL NOT NULL);"

create_formula = "CREATE TABLE formula (username TEXT PRIMARY KEY, lang TEXT NOT NULL, sortAlg TEXT NOT NULL, type TEXT NOT NULL, bitcoin TEXT NOT NULL, nameCase TEXT NOT NULL, braces TEXT NOT NULL, bio TEXT NOT NULL, open DECIMAL NOT NULL, consc DECIMAL, extra DECIMAL, agree DECIMAL, emotRange DECIMAL);"

#create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);"
insert_admin = "INSERT INTO users VALUES ('test', encrypt('test'), 'test', '18', 'Male', 'Male', 'Java', 'Merge Sort', 'OOP', 'No', 'snake_case', 'First', 'blah blah bio');"


#insert_admin = "INSERT INTO users VALUES ('test', encrypt('test'));"

try:
    c.execute(create_users)
    c.execute(create_personality)
    c.execute(create_formula)
    c.execute(insert_admin)

except:
    pass

db.commit() #save changes
#db.close()  #close database
