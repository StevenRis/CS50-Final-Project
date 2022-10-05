from flask import Flask, render_template, redirect, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars")
def cars():
    return render_template("cars.html")


@app.route("/locations")
def locations():
    """Show locations"""

    connection = sql.connect("test.db")
    connection.row_factory = sql.Row

    db = connection.cursor()
    locations = db.execute("SELECT * FROM locations")

    # rows = db.fetchall()
    return render_template("locations.html", locations=locations)


# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)