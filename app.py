from datetime import datetime
import re
from flask import Flask, render_template, request, redirect, url_for
from liveserver import LiveServer


app = Flask(__name__)
ls = LiveServer(app)


@app.route('/')
def hello_world():
    list_names = ['name1', 'name2', 'name3']
    return render_template('index.html', list_names=list_names)


@app.route('/result/<string:name>')
def result(name):
    return render_template('result.html', name=name)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        name = request.form['name']
        return redirect(url_for('result', name=name))
    list_names = ['name1', 'name2', 'name3']
    return render_template('profile.html', names=list_names)


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return ls.render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/about/")
def about():
    return "Hello about"


# render_template("templates/about.html")
if __name__ == '__main__':
    app.run(debug=True)
