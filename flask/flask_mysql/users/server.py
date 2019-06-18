from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/users/new')
def new():
    return render_template("new.html")   

@app.route('/users')
def index():
    mysql = connectToMySQL("users")
    query = "SELECT * FROM users"
    all_users = mysql.query_db(query)
    return render_template("users.html", all_users = all_users)

@app.route('/users/<user_id>/edit')
def edit(user_id):
    mysql = connectToMySQL("users")
    query = "SELECT * from users WHERE id = %(id)s"
    data = {
        'id' : user_id
    }
    user_edit = mysql.query_db(query,data)
    return render_template("edit.html", user_edit = user_edit)

@app.route('/users/create', methods = ['POST'])
def create():
    mysql = connectToMySQL("users")
    query = "INSERT INTO USERS (first_name, last_name, email, created_at, updated_at) values (%(first_name)s,%(last_name)s ,%(email)s, now(), now())"
    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email']
    }
    user_id = mysql.query_db(query, data)
    return redirect('/users/' + str(user_id))

@app.route('/users/<user_id>')
def show(user_id):
    mysql = connectToMySQL("users")
    query = "SELECT * from users WHERE id = %(id)s"
    data = {
        'id' : user_id
    }
    user = mysql.query_db(query,data)
    return render_template("userinfo.html",user=user)

@app.route('/users/<user_id>/destroy')
def destroy(user_id):
    mysql = connectToMySQL("users")
    query = "DELETE FROM users WHERE id = %(id)s"
    data = {
        'id' : user_id
    }
    mysql.query_db(query, data)
    return redirect('/users')

@app.route('/users/<user_id>/update', methods = ['POST'])
def update(user_id):
    mysql = connectToMySQL("users")
    query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = now() WHERE id = %(id)s"
    data = {
        'id' : user_id,
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email']
    }
    mysql.query_db(query,data)
    return redirect('/users/' + str(user_id))

if __name__ == "__main__":
    app.run(debug=True)