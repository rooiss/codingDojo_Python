from flask import Flask, render_template, redirect, request, flash
import re
from mysqlconnection import connectToMySQL
app=Flask(__name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
app.secret_key = "WOOT"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    is_valid = True
    # if len(request.form['name']) < 3:
    #     is_valid = False
    #     flash("Name must be at least 3 characters")
    
    if len(request.form['email']) < 1:
        is_valid = False
        flash("You left email blank")

    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Enter valid email address")

    if not is_valid:
        return redirect('/')

    if is_valid:
        mysql = connectToMySQL("emailvalidation")
        query = "INSERT INTO users (email) VALUES (%(email)s)"
        data = {
            "email" : request.form["email"]
        }
        user = mysql.query_db(query,data)
        return render_template("success.html", user=user)



if __name__ == "__main__":
    app.run(debug=True)
