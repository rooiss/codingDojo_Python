from flask import Flask, render_template
app = Flask(__name__)

@app.route('/play')
def index():
    return render_template("index.html")

@app.route('/play/<times>')
def times(times):
    return render_template("index.html", num_times=int(times))

@app.route('/play/<times>/<color>')
def coloring(times, color):
    return render_template("index.html", num_times=int(times), background_color=(color))


if __name__ =="__main__":
    app.run(debug=True)