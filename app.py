import sqlite3

from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)


def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3'):
        g.sqlite_db.close()


@app.route('/')
def hello_world():
    db = get_db()
    cur = db.execute('select id, name, surname, age from user')
    query = cur.fetchall()
    return render_template('index.html', query=query)


@app.route('/delete/<user_id>')
def delete_user(user_id):
    db = get_db()
    db.execute('delete from user where id=?', [user_id])
    db.commit()
    return redirect(url_for('hello_world'))


@app.route('/update_user/<user_id>', methods=["post", 'get'])
def update_user(user_id):
    if request.method == 'POST':
        db = get_db()
        new_name = request.form.get('new_name')
        db.execute('update user set name=? where id=?', [new_name, user_id])
        db.commit()
        return redirect(url_for('hello_world'))


@app.route('/result', defaults={'name': "Default"})
@app.route('/result/<string:name>')
def result(name):
    return render_template('result.html', name=name)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == "POST":
        db = connect_db()
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']

        db.execute('insert into user (name, surname, age) values (?, ?, ?)', [
                   name, surname, age])
        db.commit()

        return redirect(url_for('result', name=name))
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)
