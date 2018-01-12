import sqlite3   #enable control of an sqlite database

def openDb(path):
    db = sqlite3.connect(path)
    return db

def createCursor(db):
    c = db.cursor()
    return c

def commit(db):
    db.commit()

def closeFile(db):
    db.close()

#NOTE: when putting in a string in the values array u have to do this: "'josh'"
#values is an array with values to insert for that row
def insertRow (tableName, fields, values, cursor):
    parameter = ' ('

    for field in fields:
        parameter += field + ", "
    parameter = parameter[0:-2] + ") VALUES ("
    #print parameter

    for value in values:
        val = str(value)
        if isinstance(value, basestring):
            val = "'" + val + "'"
        parameter += val + ", "
    parameter = parameter[0:-2] + ");"

    insert = "INSERT INTO " + tableName + parameter
    print "\n\n" + insert + "\n\n"

    cursor.execute(insert)



#condition is string type and follows WHERE statement for UPDATE
def update (tableName, field, newVal, condition, cursor):
    update = "UPDATE " + tableName + " SET " + field + " = " + str(newVal)
    if len(condition) != 0:
        update += " WHERE " + condition + ";"

    print "\n\n" + update + "\n\n"
    cursor.execute(update)

def table_gen(c):
    #sad, joy, angry/disgust, fear are the most recent song recommendation for this user for each mood
    create_users = "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT,sadness TEXT, joy TEXT, anger TEXT,fear TEXT);"
    
    #mood will be a dictionary, song rating is either one,two,three (two by default)
    create_diary = "CREATE TABLE IF NOT EXISTS diary(username TEXT, date TEXT, entry TEXT, mood TEXT, song TEXT, songRating TEXT);"

    #for base songs the parentSong field will contain "base"
    create_songs = "CREATE TABLE IF NOT EXISTS songs(song TEXT,artist TEXT, mood TEXT, one TEXT, two TEXT, three TEXT, parentSong TEXT);"
    
    c.execute(create_users)
    c.execute(create_diary)
    c.execute(create_songs)
#============================================================================================
if __name__ == "__main__":
    db = openDb("data/tunes.db")
    c = createCursor(db)
    table_gen(c)

    #filling in some sad songs in the songs table
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["let it be", "the beatles", "sadness" ,"im not the only one" , "base"],c)
    insertRow("songs", ['song', 'artist', 'mood','two','parentSong'], ["im not the only one", "sam smith", "sadness","she will be loved", "let it be"],c)
    insertRow("songs", ['song', 'artist', 'mood', 'parentSong'], ["she will be loved", "maroon 5", "sadness", "im not the only one"],c)

    #filling in some happy songs in the songs table
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["uptown funk", "mark ronson", "joy" ,"different colors" , "base"],c)
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["different colors", "walk the moon", "joy" ,"unbelievers" , "uptown funk"],c)
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["unbelievers", "vampire weekend", "joy" ,"summer" , "different colors"],c)
    insertRow("songs",['song', 'artist', 'mood', 'parentSong'], ["summer", "calvin harris", "joy" , "unbelievers"],c)

    #filling in some calming song (for fear mood) in the songs table
    insertRow("songs",['song', 'artist', 'mood','two', 'parentSong'], ["how to save a life", "the fray", "fear" ,"i wont give up" , "base"],c)
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["i wont give up", "jason mraz", "fear" ,"eine kleine nachtmusik" , "how to save a life"],c)
    insertRow("songs",['song', 'artist', 'mood', 'parentSong'], ["eine kleine nachtmusik", "wolfgang amadeus mozart", "fear" ,"i wont give up"],c)

    #filling in some intense songs (for angry/disgusted) in the songs table
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["smells like teen spirit", "nirvana", "anger" ,"revolution" , "base"],c)
    insertRow("songs",['song', 'artist', 'mood','one', 'parentSong'], ["revolution", "the beatles", "anger" ,"till i collapse" , "smells like teen spirit"],c)
    insertRow("songs",['song', 'artist', 'mood','one','parentSong'], ["till i collapse", "eminem", "anger","we will rock you", "revolution"],c)
    insertRow("songs",['song', 'artist', 'mood', 'parentSong'], ["we will rock you", "queen", "anger","till i collapse"],c)


    commit(db)
    closeFile(db)


