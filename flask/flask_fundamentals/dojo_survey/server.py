from flask import Flask, render_template, request, flash, session, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "keep it a secret"
@app.route('/')
def index():
    mysql = connectToMySQL("survey")
    users = mysql.query_db("SELECT * FROM user;")
    return render_template("index.html", users = users)

@app.route("/process", methods=["POST"])
def add_user_to_db(): 
    is_valid = True
    if len(request.form["username"]) < 1:
        is_valid = False
        flash("Please enter a name")
    if is_valid:
        query = "INSERT INTO USER (username, location, language) values (%(username)s,%(location)s,%(language)s)"
        data = {
            'username' : request.form['username'],
            'location' : request.form['location'],
            'language' : request.form['language']
        }
        mysql = connectToMySQL("survey")
        id = mysql.query_db(query,data)
        return redirect(f"/show/{id}")
    return redirect("/")

@app.route('/show/<id>')
def show(id):
    mysql = connectToMySQL("survey")
    query = "SELECT * from user WHERE id = %(id)s"
    data = {
        "id" : id
    }
    users = mysql.query_db(query,data)
    print(users)
    return render_template("show.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
