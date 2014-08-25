import sqlite3
import json
from app import app, get_db
from datetime import datetime as datetime
from flask import render_template, request, url_for, redirect, session, g, \
    flash, abort, jsonify, Response

now = None
@app.route('/test', methods = ['GET'])
def test():
    jstime = int(request.args.get('time'))
    pydate = datetime.fromtimestamp(jstime/1000)
    if now is not None:
        print(now > pydate)
        print('now', now)
        print('pyd', pydate)
    mylist = []
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    #cur = db.execute('select title, text from entries order by id desc limit 1')
    entries = cur.fetchall()
    for entry in entries:
        mydict = []
        print(entry[0])
        print(entry[1])
        mydict.append(entry[0])
        mydict.append(entry[1])
        mylist.append(mydict)
    return Response(json.dumps(mylist))

@app.route('/')
def show_entries():
    """gets a db and executes a SQL statement
    fetchall() - fetches all rows of a query result - returns a list
    """
    #db = get_db()
    #cur = db.execute('select title, text from entries order by id desc')
    #entries = cur.fetchall()
    return render_template('show_entries.html')

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'): # if user types /add at end of URL
        abort(401) #unauthorized http
    if request.form['title'] != '' or request.form['text'] != '':
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
                [request.form['title'], request.form['text']])
        # (?, ?) - used to avoid SQL injection
        db.commit()
        global now
        now = datetime.now()
        flash('New entry successfully posted!')
    else:
        flash('Must enter a title and text')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
            request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid credentials'
        else:
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('show_entries'))
