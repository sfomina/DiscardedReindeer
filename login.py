from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
import os, sqlite3, hashlib
from utils import api_library, dbLibrary
from werkzeug.utils import secure_filename

SUCCESS = 1
BAD_PASS = -1
BAD_USER = -2

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


form_site = Flask(__name__)
form_site.secret_key = os.urandom(64)
form_site.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


execfile("db_builder.py")

#===========HELPERS=============================================

#encrypts password
def encrypt_password(password):
    encrypted_pass = hashlib.sha1(password.encode('utf-8')).hexdigest()
    return encrypted_pass

#create dict of usernames and passwords
def user_dict():
    users = {} #{username: password}
    user_data = c.execute("SELECT * FROM users;")
    for data in user_data:
        users[data[0]] = data[1]
    return users;


#authenticate username and password
def authenticate(username, password):
    users = user_dict()
    if username in users.keys():
        if password == users[username]:
            return SUCCESS
        else:
            return BAD_PASS
    else:
        return BAD_USER

#check if username already exists
def check_newuser(username):
    users = user_dict()
    if username in users.keys():
        return BAD_USER
    return SUCCESS

#checks for allowed files
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#============================================

@form_site.route('/', methods=['POST', 'GET'])
#login page if user is not in session, otherwise welcome
def root():
    if 'user' not in session:
        return render_template('login.html', title="Login")
    else:
        return redirect( url_for('welcome') )

@form_site.route('/register', methods=['POST', 'GET'])
#register page is user is not in session, otherwise root
def register():
    if 'user' not in session:
        return render_template('register.html', title="Register")
    else:
        return redirect( url_for('root') )



@form_site.route('/createaccount', methods=['POST', 'GET'])
#creates an account and runs encryption function on password
def create_account():
    username = request.form['user']
    password = request.form['pw']
    name = request.form['inputName']
    age = request.form['age']
    prefGender = request.form['prefGender']
    gender = request.form['gender']
    lang = request.form ['lang']
    sort = request.form['sort']
    progType = request.form['type']
    bitcoin = request.form['bitcoin']
    case = request.form['case']
    braces = request.form['braces']
    bio = request.form['bio']
    result = check_newuser(username)
    users = user_dict()
    img_name = ''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            extension = file.filename.split(".")[1]
            filename = username + "." + extension;
            print filename
            file.save(os.path.join(form_site.config['UPLOAD_FOLDER'], filename))
            img_name = filename
    if result == SUCCESS:
        with db:
            c.execute("INSERT INTO users (username, password, name, age, gender, prefGender, lang, sortAlg, type, bitcoin, nameCase, braces, bio, img_name) VALUES (?, encrypt(?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)", (username, password, name, age,gender, prefGender, lang, sort, progType, bitcoin, case, braces , bio, img_name ))

            users[username] = password
            #form personality profile
            dbLibrary.update("users", "img_name" , "'" + filename + "'", "username = '" + username + "'", c)
            dbLibrary.update("users", "suggested" , "''", "username = '" + username + "'", c)
            dbLibrary.update("users", "queue" , "''","username = '" + username + "'", c)
            dbLibrary.update("users", "liked" , "''", "username = '" + username + "'", c)
            dbLibrary.update("users", "secured" , "''", "username = '" + username + "'", c)
            dbLibrary.insertRow("formula", ["username", "openCo" , "conscCo", "extraCo" , "agreeCo", "emotRangeCo", "challengeCo", "curiosityCo", "excitementCo", "harmonyCo", "idealCo", "libertyCo", "loveCo", "practicalityCo", "expressionCo", "stabilityCo", "structureCo", "csCo"],[ username , 1 ,1 ,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0.1] ,c)
        api_library.create_profile(username, bio)
        api_library.find_match(username)
        flash(username + " registered.")

    elif result == BAD_USER:
        flash("That username is already in use. Try another one")

    return redirect(url_for('root'))

@form_site.route('/auth', methods=['POST', 'GET'])
#checks if login information is correct
def auth():
    username = request.form['user']
    password = request.form['pw']
    encrypted = encrypt_password(password)
    result = authenticate(username, encrypted)
    if result == SUCCESS:
        session['user'] = username
        flash(session['user'] + " successfully logged in.")
    if result == BAD_PASS:
        flash("Incorrect password.")
    elif result == BAD_USER:
        flash("Incorrect Username.")
    return redirect(url_for('root'))


#FACE++API STUFF:
#url = "https://api-us.faceplusplus.com/facepp/v3/compare?api_key=" + <api_key> + "&api_secret=" + <api_secret> + "&image_file1=" + send_from_directory(form_site.config['UPLOAD_FOLDER'], <IMG_NAME OF TARGET USER>) + "&img_file2=" + send_from_directory(form_site.config['UPLOAD_FOLDER'], <IMG_NAME OF TARGET USER>)
#u = urllib2.urlopen(url)
#contents = u.read()
#similarity = json.loads(contents)['confidence']


@form_site.route('/welcome', methods=['POST', 'GET'])
#welcomes user or redirects back to root if logged out
def welcome():
    if 'user' not in session:
        return redirect( url_for('root') )
    else:
        username = session['user']
        db = dbLibrary.openDb("dating.db")
        cursor = dbLibrary.createCursor(db)
        posMatch = cursor.execute("SELECT posMatch FROM users WHERE username = '" + username + "';").fetchall()[0][0]
        if posMatch == "none":
            posMatch = api_library.find_match(username)

        if posMatch != "none":
            name = c.execute("SELECT name FROM users WHERE username = '" + posMatch + "';").fetchall()[0][0]
            bio =  c.execute("SELECT bio FROM users WHERE username = '" + posMatch + "';").fetchall()[0][0]
            percent = c.execute("SELECT percent FROM users WHERE username = '" + session['user'] + "';").fetchall()[0][0]
            image = c.execute("SELECT img_name FROM users WHERE username = '" + posMatch + "';").fetchall()[0][0]
            #percent_sim = c.execute("SELECT img_name FROM users WHERE username = '" + posMatch + "';").fetchall()[0][0]
            print image

            print "\n\n"
            print "YOUR MATCH: " + name
            print "\n\n"

            return render_template('welcome.html', user=session['user'], title='Welcome', name = name, bio = bio, percent = percent, image = "static/" + image)
        else:
            return render_template('welcome.html', user=session['user'], title='Welcome', match = "none")

@form_site.route('/matches', methods=['POST', "get"])
def matches():
    matches = c.execute("SELECT secured FROM users WHERE username = '" + session['user'] + "';").fetchall()[0][0]
    #print "matches: " + matches
    matches = matches.split(',')
    matches = filter (None, matches)
    #print len(matches)
    if (len(matches) == 0):
        flash("There are no matches to display, yet. Keep swiping!")
    return render_template('matches.html', matches = matches)


@form_site.route('/logout', methods=['POST', "get"])
#removes user from session
def logout():
    if 'user' in session:
        flash(session['user'] + " logged out.")
        session.pop('user')
    return redirect( url_for('root') )

@form_site.route('/left', methods=['POST', "get"])
def left():
    username = session['user']
    api_library.adjust_formula(username)
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)
    dbLibrary.update("users" , "posMatch" , "'none'" , "username = '" + username + "'", cursor)
    dbLibrary.commit(db)
    dbLibrary.closeFile(db)
    return redirect(url_for('welcome'))

@form_site.route('/right', methods=['POST', "get"])
def right():
    username = session['user']
    db = dbLibrary.openDb("dating.db")
    cursor = dbLibrary.createCursor(db)
    posMatch = cursor.execute("SELECT posMatch FROM users WHERE username ='" + username + "';").fetchall()[0][0]
    api_library.like(username, posMatch)
    dbLibrary.update("users" , "posMatch" , "'none'" , "username = '" + username + "'", cursor )
    dbLibrary.commit(db)
    dbLibrary.closeFile(db)
    return redirect(url_for('welcome'))

@form_site.route('/', defaults={'path': ''})
@form_site.route('/<path:path>')
def catch_all(path):
    flash ("Sorry! The page you tried to visit does not exist!")
    return redirect(url_for('root'))




if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

db.commit()
db.close()
