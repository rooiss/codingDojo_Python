from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/dojo')
def dojo():
    return "Dojo!"

@app.route('/hi/<name>')
def hi(name):
    print(name)
    return ("Hi " + name + "!")

@app.route('/repeat/<num>/<name>')
def repeat(num,name):
    print(name)
    return (int(num) * name)

if __name__ =="__main__":
    app.run(debug=True)