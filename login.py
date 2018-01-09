from flask import Flask, render_template, request, session, redirect, url_for, flash
import os, sqlite3, hashlib

SUCCESS = 1
BAD_PASS = -1
BAD_USER = -2

form_site = Flask(__name__)
form_site.secret_key = os.urandom(64)

execfile("db_builder.py")

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

#create dict of edit history
def history_dict():
    history = {} #{id: {username: contribution}}
    history_data = c.execute("SELECT * FROM history;")
    for data in history_data:
        try:
            history[data[1]][data[0]] = data[2]
        except:
            history[data[1]] = {data[0]: data[2]}
    return history;

#create dict of story info
def story_dict():
    stories = {} #{id: {title: title, fullstory: fullstory, previousupdate: previousupdate}}
    stories_data = c.execute("SELECT * FROM stories;")
    for data in stories_data:
        try:
            stories[data[0]]["title"] = data[1]
            stories[data[0]]["fullstory"] = data[2]
            stories[data[0]]["previousupdate"] = data[3]
        except:
            stories[data[0]] = {"title": data[1], "fullstory": data[2], "previousupdate": data[3]}
    return stories;

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
    result = check_newuser(username)
    users = user_dict()
    if result == SUCCESS:
        with db:
            c.execute("INSERT INTO users VALUES (?, encrypt(?))", (username, password))
        users[username] = password
        flash(username + " registered.")
    elif result == BAD_USER:
        flash("That username is already in use. Try another one")
        return redirect(url_for('register'))
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

@form_site.route('/welcome', methods=['POST', 'GET'])
#welcomes user or redirects back to root if logged out
def welcome():
    if 'user' not in session:
        return redirect( url_for('root') )
    else:
        return render_template('welcome.html', user=session['user'], title='Welcome')

@form_site.route('/logout', methods=['POST', "get"])
#removes user from session
def logout():
    if 'user' in session:
        flash(session['user'] + " logged out.")
        session.pop('user')
    return redirect( url_for('root') )

@form_site.route('/editstory', methods=['POST', 'GET'])
#commits story changes to db
def edit_story():
    #print request.form
    #print "TTTTTTTTT"
    #print request.form['id']
    #c.execute("DELETE FROM history WHERE contribution='hello';")
    stories = story_dict()
    if "user" not in session:
        flash("You must login to edit story")
    else:

        #print "##########################################################"
        #print stories[int(request.form['id'])]["fullstory"]
        #print request.form['contribution']
        #print stories[int(request.form['id'])]["fullstory"] + request.form['contribution']
        #print "##########################################################"
        with db:
            c.execute("INSERT INTO history VALUES (?, ?, ?)", (session['user'], request.form['id'], request.form['contribution']))
            c.execute("UPDATE stories SET fullstory=? WHERE id=?", (stories[int(request.form['id'])]["fullstory"] + "\n" + request.form['contribution'], request.form['id']))
            c.execute("UPDATE stories SET previousupdate=? WHERE id=?", (request.form['contribution'], request.form['id']))
        flash("Story edited.")
    #INSERT FLASH HERE***************************************
    return redirect( url_for('root') )

@form_site.route('/choseneditstory', methods=['POST', 'GET'])
#takes user to the page where they can edit the story they chose
def chosen_edit_story():
    stories = story_dict()

    #print request.form.keys()
    #print request.form.values()
    #print request.form.keys()[0]
    #print request.form.values()[0]
    #print stories
    #print stories[request.form.keys()[0]]

    if "user" not in session:
        flash("You must login to edit story")
        return redirect (url_for("root"))
    else:
        previous = stories[int(request.form.values()[0])]["previousupdate"]
        #print previous
        id = int(request.form.values()[0])
        #print "----------"
        #print "----------"
        return render_template("edit_story.html", id=id, title=stories[int(request.form.values()[0])]["title"], previous=previous)

@form_site.route('/chooseeditstory', methods=['POST', 'GET'])
#creates a list of stories that the user is allowed to edit
def choose_edit_story():
    stories = story_dict()
    history = history_dict()
    new = {}
    if "user" not in session:
        flash("You must login to edit story")
        return redirect (url_for("root"))
    else:
        for story in stories.keys():

            #print "===================="
            #print story
            #print session['user']
            #print history[story].keys()
            #print "===================="

            if session['user'] not in history[story].keys():
                    new[story] = stories[story]["title"]
        if not new:
            flash ("There are no new stories to edit (You may only edit stories that you have not created or edited before!)")
        return render_template('list.html', title="Edit Stories!", new=new, action="edit", actionurl = "/choseneditstory")

@form_site.route('/createstoryhome', methods=['POST', 'GET'])
#takes user to the page where they can create a story
def newstory():
    if "user" not in session:
        flash("You must login to create a story")
        return redirect (url_for("root"))
    return render_template('create_story.html')

@form_site.route('/createstory', methods=['POST', 'GET'])
#commits new story to db
def create():
    if 'user' not in session:
        flash("You must log in to create a story")
    else:
        title = request.form["title"]
        line = request.form["firstline"]
        last_entry = c.execute("SELECT * FROM stories WHERE ID = (SELECT MAX(ID) FROM stories);")
        for value in last_entry:
            id = value[0] + 1;
            #successfully updates stories database
        with db:
            c.execute("INSERT into stories VALUES (?, ?, ?, ?)", (id, title, line, line))
            c.execute("INSERT into history VALUES (?, ?, ?)", (session['user'], id, line))
        flash("Your story was succesfully created!")
    return redirect(url_for('root'))


@form_site.route('/viewstories', methods = ['POST', 'GET'])
#creates a list of stories that the user is allowed to view
def viewstory():
    stories = story_dict()
    history = history_dict()
    new = {}
    if 'user' not in session:
        flash("You must log in to view stories")
        return redirect(url_for('root'))
    else:
        for story in stories:
            if session['user'] in history[story].keys():
                new[story] = stories[story]["title"]
        if not new:
            flash ("There are no stories to view (You may only view stories that you have edited before!)")

        return render_template("list.html", new = new, action="view", actionurl = "/display")

@form_site.route('/display', methods = ['POST', 'GET'])
#displays the story that the user chose to view
def displaypage():
    if 'user' not in session:
        flash("You must log in to view stories")
        return redirect(url_for('welcome'))
    idnum = request.form.get('id')
    storyinfo = c.execute("SELECT * FROM stories where ID = ?", (idnum,)).fetchall()
    title = storyinfo[0][1]
    fullstory = storyinfo[0][2]
    listy = fullstory.splitlines()
    return render_template("display.html", title = title, story = fullstory, id = idnum, lines=listy)

if __name__ == '__main__':
    form_site.debug = True
    form_site.run()

db.commit()
db.close()
