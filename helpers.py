import sqlite3
from flask import redirect, render_template, request, session
from functools import wraps

# con = sqlite3.connect("database.db")

# con.execute('''CREATE TABLE locations (id INTEGER PRIMARY KEY,
# location TEXT,
# FOREIGN KEY (id) REFERENCES cars(id))''')
# con.execute('INSERT INTO cars (car_brand, car_model) VALUES ("Ford", "Focus")')
# con.commit()

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
