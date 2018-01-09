import sqlite3, hashlib   #enable control of an sqlite database

f="story.db"

def encrypt_password(password):
    encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
    #print encrypted_pass
    return encrypted_pass

db = sqlite3.connect(f, check_same_thread=False) #open if f exists, otherwise create
db.create_function('encrypt', 1, encrypt_password)
c = db.cursor()    #facilitate db ops

create_users = "CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL);"


insert_admin = "INSERT INTO users VALUES ('test', encrypt('test'));"

#insert_admin0 = "INSERT INTO users VALUES ('test', encrypt('test'));"
#insert_history0 = "INSERT INTO history VALUES ('test0', 0, 'hi0');"
#insert_history1 = "INSERT INTO history VALUES ('test0', 1, 'new');"
#insert_newstory = "INSERT INTO stories VALUES (1, 'new title', 'new', 'new')"

try:
    c.execute(create_users)
    c.execute(insert_admin)
    #c.execute(insert_admin0)
    #c.execute(insert_history0)
    #c.execute(insert_newstory)
    #c.execute(insert_history1)
except:
    pass

db.commit() #save changes
#db.close()  #close database
