from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "thereisnospoon"

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    is_valid = True
    if len(request.form["fname"]) == 0:
        is_valid = False
        flash("This is a required field", "fname")
    elif len(request.form["fname"]) < 2:
        is_valid = False
        flash("First name must be at least 2 characters", "fname")
    elif not NAME_REGEX.match(request.form["fname"]):
        is_valid = False
        flash("First name must contain only letters", "fname")
    if len(request.form["lname"]) == 0:
        is_valid = False
        flash("This is a required field", "lname")
    elif len(request.form["lname"]) < 2:
        is_valid = False
        flash("Last name must be at least 2 characters", "lname")
    elif not NAME_REGEX.match(request.form["lname"]):
        is_valid = False
        flash("Last name must contain only letters", "lname")
    if len(request.form["email"]) == 0:
        is_valid = False
        flash("This is a required field", "email")
    elif not EMAIL_REGEX.match(request.form["email"]):
        is_valid = False
        flash("Invalid email address!!", "email")
    if len(request.form["pass"]) == 0:
        is_valid = False
        flash("This is a required field", "pass")
    elif len(request.form["pass"]) < 8:
        is_valid = False
        flash("Password must be at least 8 characters!!", "pass")
    if request.form["pass2"] != request.form["pass"]:
        is_valid = False
        flash("Passwords must match!!", "pass2")
    if is_valid:
        print("Got Post Info")
        print(request.form)
        session["first"] = request.form["fname"]      # store first name in session if we need to call on it
        session["justregistered"] = True              # store a check that someone had just registered if we want to send a special msg
        password = bcrypt.generate_password_hash(request.form['pass']) 
        print(password)
        mysql = connectToMySQL("beltexam")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s);"
        # put the pw_hash in our data dictionary, NOT the password the user provided
        data = { 
            "fn" : request.form["fname"],
            "ln" : request.form["lname"],
            "em" : request.form["email"],
            "pw" : password
        }
        session["userid"] = mysql.query_db(query, data)
        # mysql.query_db(query, data)
        return redirect("/dashboard")
    else:
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    is_valid = True
    if len(request.form["loginemail"]) == 0:
        flash("This is a required field", "logemail")
    if len(request.form["loginpass"]) == 0:
        flash("This is a required field", "logpass")
    if is_valid:
        mysql = connectToMySQL("beltexam")
        query = "SELECT * FROM users WHERE email = %(em)s;"
        data = { "em" : request.form["loginemail"] }
        result = mysql.query_db(query, data)
        if len(result) > 0:
            if bcrypt.check_password_hash(result[0]['password'], request.form['loginpass']):
                session["userid"] = result[0]["users_id"]
                session["first"] = result[0]["first_name"]
                print(session["first"])
                return redirect('/dashboard')
    flash("You could not be logged in", "loginfail")
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    mysql = connectToMySQL("beltexam")
    query = "SELECT * from jobs"
    all_jobs = mysql.query_db(query)

    return render_template("dashboard.html", all_jobs = all_jobs)

@app.route('/new')
def createnew():
    return render_template("new.html")

@app.route('/jobs/<jobs_id>')
def showjob(jobs_id):
    mysql = connectToMySQL("beltexam")
    query = "SELECT * FROM jobs JOIN users ON users.users_id = jobs.users_id WHERE jobs_id = %(id)s;"
    data = {
        'id' : jobs_id,
    }
    showjob = mysql.query_db(query,data)
    return render_template("jobs.html", showjob=showjob)

@app.route('/edit/<jobs_id>')
def edit(jobs_id):
    mysql = connectToMySQL("beltexam")
    query = "SELECT * FROM jobs WHERE jobs_id = %(id)s"
    data = {
        'id' : jobs_id,
    }
    jobs = mysql.query_db(query,data)
    return render_template("edit.html", jobs=jobs)

@app.route('/update/<jobs_id>', methods=['POST'])
def update(jobs_id):
    is_valid = True
    if len(request.form["title"]) < 3:
        is_valid = False
        flash("A job must consist of 3 or more characters")
    if len(request.form["description"]) < 3:
        is_valid = False
        flash("A description must consist of 3 or more characters")
    if len(request.form["location"]) < 3:
        is_valid = False
        flash("A location must consist of 3 or more characters")
    if is_valid == False:
        return redirect(f'edit/{jobs_id}')
    if is_valid:
        mysql = connectToMySQL("beltexam")
        query = "UPDATE jobs SET title = %(title)s, description = %(description)s, location = %(location)s WHERE jobs_id = %(id)s;"
        data = {
            'id' : jobs_id,
            'title' : request.form['title'],
            'description' : request.form['description'],
            'location' : request.form['location']
        }
        mysql.query_db(query,data)
        return redirect('/dashboard')

@app.route("/create", methods=['POST'])
def create():
    is_valid = True
    if len(request.form["title"]) < 3:
        is_valid = False
        flash("A job must consist of 3 or more characters")
    if len(request.form["description"]) < 3:
        is_valid = False
        flash("A description must consist of 3 or more characters")
    if len(request.form["location"]) < 3:
        is_valid = False
        flash("A location must consist of 3 or more characters")
    if is_valid == False:
        return redirect('/new')
    if is_valid:
        mysql = connectToMySQL("beltexam")
        query = "INSERT INTO jobs (title, description, location, users_id) VALUES (%(title)s, %(description)s, %(location)s, %(users_id)s);"
        data = {
            "users_id" : session["userid"],
            "title" : request.form["title"],
            "description" : request.form["description"],
            "location" : request.form["location"]
        }
        mysql.query_db(query,data)
        return redirect('/dashboard')

@app.route('/remove/<jobs_id>')
def removefromlist(jobs_id):
    mysql = connectToMySQL("beltexam")
    query = "DELETE FROM jobs WHERE jobs_id = %(id)s"
    data = {
        'id' : jobs_id
    }
    mysql.query_db(query,data)
    return redirect('/dashboard')

if __name__ == "__main__":
    app.run(debug=True)