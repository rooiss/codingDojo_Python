from flask import Flask, render_template, redirect, session, request
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route("/")
def index():
    mySQL = connectToMySQL('pets')
    pets = mySQL.query_db('SELECT * FROM pets;')
    print(pets)
    return render_template('index.html', pets=pets)

@app.route('/create_pet', methods=['POST'])
def create_pet():
    query = ('INSERT INTO pets (name,type) VALUE (%(n)s, %(t)s);')
    data = {
        'n': request.form['name'],
        't': request.form['type']
    }
    db = connectToMySQL('pets')
    db.query_db(query, data)

    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)
