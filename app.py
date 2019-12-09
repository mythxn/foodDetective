import sqlite3

from flask import Flask, redirect, request, url_for, render_template, session

# create an app
app = Flask(__name__)  # our Flask app
DB_FILE = 'mydb.db'  # file for our Database
app.secret_key = "super secret key"


# set-up index page
@app.route('/')
def root():
    return render_template('index.html')


# # setup posts
# @app.route('/posts/1')
# def post1():
#     return render_template('posts/1.html')
#
#
# @app.route('/posts/2')
# def post2():
#     return render_template('posts/2.html')
#
#
# @app.route('/posts/3')
# def post3():
#     return render_template('posts/3.html')


# guestbook
def _insert(name, email, comment):
    params = {'name': name, 'email': email, 'comment': comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("insert into guestbook VALUES (:name, :email, :comment)", params)
    connection.commit()
    cursor.close()


@app.route('/guestbook', methods=['POST', 'GET'])
def gb():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM guestbook")
    rv = cursor.fetchall()
    cursor.close()
    return render_template('guestbook.html', entries=rv)


@app.route('/sign', methods=['POST'])
def sign():
    _insert(request.form['name'], request.form['email'], request.form['comment'])
    return redirect(url_for('gb'))


# register
@app.route('/reg')
def reg():
    return render_template('reg.html')


def _newaccount(username, email, password):
    params = {'username': username, 'email': email, 'password': password}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("insert into accounts VALUES (:username, :email, :password)", params)
    connection.commit()
    cursor.close()


@app.route('/register', methods=['POST'])
def register():
    _newaccount(request.form['username'], request.form['email'], request.form['password'])
    return redirect(url_for('reg'))


# login
@app.route('/login')
def login():
    return render_template('login.html')


# sign-in
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        query = "select * from accounts where username = '" + request.form['username']
        query = query + "' and password = '" + request.form['password'] + "';"
        connection = sqlite3.connect(DB_FILE)
        cur = connection.execute(query)
        rv = cur.fetchall()
        cur.close()
        if len(rv) == 1:
            session['username'] = request.form['username']
            session['logged in'] = True
            return redirect("/")
        else:
            return render_template('login.html', msg="Check your login details and try again.")
    else:
        return render_template('login.html')


# logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("logged in", None)
    session.pop("username", None)
    return render_template('index.html')


# comment1
@app.route('/posts/1', methods=['POST', 'GET'])
def posts1():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM post1")
    rv = cursor.fetchall()
    cursor.close()
    return render_template('/posts/1.html', entries=rv)


def _newcomment1(username, comment):
    params = {'username': username, 'comment': comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("insert into post1 VALUES (:username, :comment)", params)
    connection.commit()
    cursor.close()


@app.route('/comment1', methods=['POST'])
def comment1():
    _newcomment1(session['username'], request.form['comment'])
    return redirect(url_for('posts1'))


# comment2
@app.route('/posts/2', methods=['POST', 'GET'])
def posts2():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM post2")
    rv = cursor.fetchall()
    cursor.close()
    return render_template('/posts/2.html', entries=rv)


def _newcomment2(username, comment):
    params = {'username': username, 'comment': comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("insert into post2 VALUES (:username, :comment)", params)
    connection.commit()
    cursor.close()


@app.route('/comment2', methods=['POST'])
def comment2():
    _newcomment1(session['username'], request.form['comment'])
    return redirect(url_for('posts2'))


# comment3
@app.route('/posts/3', methods=['POST', 'GET'])
def posts3():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM post3")
    rv = cursor.fetchall()
    cursor.close()
    return render_template('/posts/3.html', entries=rv)


def _newcomment3(username, comment):
    params = {'username': username, 'comment': comment}
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("insert into post3 VALUES (:username, :comment)", params)
    connection.commit()
    cursor.close()


@app.route('/comment3', methods=['POST'])
def comment3():
    _newcomment1(session['username'], request.form['comment'])
    return redirect(url_for('posts3'))


if __name__ == '__main__':
    app.run(debug=True)
