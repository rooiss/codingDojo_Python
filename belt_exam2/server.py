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
        session["first"] = request.form["fname"]
        session["justregistered"] = True
        password = bcrypt.generate_password_hash(request.form['pass']) 
        print(password)
        mysql = connectToMySQL("pythonexam")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pw)s);"
        data = { 
            "fn" : request.form["fname"],
            "ln" : request.form["lname"],
            "em" : request.form["email"],
            "pw" : password
        }
        session["userid"] = mysql.query_db(query, data)
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
        mysql = connectToMySQL("pythonexam")
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
    mysql = connectToMySQL("pythonexam")
    query = "SELECT * from trips"
    all_trips = mysql.query_db(query)

    return render_template("dashboard.html", all_trips = all_trips)

@app.route('/new')
def createnew():
    return render_template("new.html")

@app.route("/create", methods=['POST'])
def create():
    is_valid = True
    if len(request.form["destination"]) < 3:
        is_valid = False
        flash("A destination must consist of 3 or more characters")
    if len(request.form["start_date"]) < 7:
        is_valid = False
        flash("You have to enter a start date!")
    if len(request.form["end_date"]) < 7:
        is_valid = False
        flash("You have to enter a end date!")
    if len(request.form["plan"]) < 3:
        is_valid = False
        flash("A plan must consist of 3 or more characters")
    if is_valid == False:
        return redirect('/new')
    if is_valid:
        mysql = connectToMySQL("pythonexam")
        query = "INSERT INTO trips (destination, start_date, end_date, plan, users_users_id) VALUES (%(destination)s, %(start_date)s, %(end_date)s, %(plan)s, %(users_users_id)s);"
        data = {
            "users_users_id" : session["userid"],
            "destination" : request.form["destination"],
            "start_date" : request.form["start_date"],
            "end_date" : request.form["end_date"],
            "plan" : request.form["plan"]
        }
        mysql.query_db(query,data)
        return redirect('/dashboard')

@app.route('/trips/<trips_id>')
def showjob(trips_id):
    mysql = connectToMySQL("pythonexam")
    query = "SELECT * FROM trips WHERE trips_id = %(id)s;"
    data = {
        'id' : trips_id,
    }
    showtrips = mysql.query_db(query,data)
    return render_template("trips.html", showtrips=showtrips)

@app.route('/edit/<trips_id>')
def edit(trips_id):
    mysql = connectToMySQL("pythonexam")
    query = "SELECT * FROM trips WHERE trips_id = %(id)s"
    data = {
        'id' : trips_id,
    }
    trips = mysql.query_db(query,data)
    return render_template("edit.html", trips=trips)

@app.route('/update/<trips_id>', methods=['POST'])
def update(trips_id):
    is_valid = True
    if len(request.form["destination"]) < 3:
        is_valid = False
        flash("A destination must consist of 3 or more characters")
    if len(request.form["start_date"]) < 7:
        is_valid = False
        flash("You have to enter a start date!")
    if len(request.form["end_date"]) < 7:
        is_valid = False
        flash("You have to enter a end date!")
    if len(request.form["plan"]) < 3:
        is_valid = False
        flash("You kinda need a plan for this trip")
    if is_valid == False:
        return redirect(f'edit/{trips_id}')
    if is_valid:
        mysql = connectToMySQL("pythonexam")
        query = "UPDATE trips SET destination = %(destination)s, start_date = %(start_date)s, end_date = %(end_date)s, plan = %(plan)s WHERE trips_id = %(id)s;"
        data = {
            'id' : trips_id,
            'destination' : request.form['destination'],
            'start_date' : request.form['start_date'],
            'end_date' : request.form['end_date'],
            'plan' : request.form['plan']
        }
        mysql.query_db(query,data)
        return redirect('/dashboard')

@app.route('/remove/<trips_id>')
def removefromlist(trips_id):
    mysql = connectToMySQL("pythonexam")
    query = "DELETE FROM trips WHERE trips_id = %(id)s"
    data = {
        'id' : trips_id
    }
    mysql.query_db(query,data)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)