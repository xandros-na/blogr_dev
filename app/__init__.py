import os
import sqlite3
from config import config
from flask import Flask, g

app = Flask(__name__)
app.config.from_object(os.environ.get('BLOGR_SETTINGS') or config['default'])

def connect_db():
    """connect to a db"""
    rv = sqlite3.connect(app.config['DATABASE_URI'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """open a new db connection if there is none for the current app context"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext #disconects the db
def close_db(error):
    """close db again at end of request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    return

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            """executes statements in schema.sql"""
            db.cursor().executescript(f.read())
        db.commit()
    return

from . import routes
