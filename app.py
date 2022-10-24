from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 as sql

from helpers import login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Connect database
def db_connection():
    connection = sql.connect("database.db")
    connection.row_factory = sql.Row
    return connection


@app.route("/")
@app.route("/home")
@login_required
def home():

    user_id = session("user_id")

    db = db_connection()
    username = db.execute("SELECT username FROM users WHERE id=?", [user_id]).fetchall()

    username = username[0]["username"]

    db.close()
    return render_template("index.html", username=username)


@app.route("/cars", methods=["GET", "POST"])
def cars():
    """Show cars"""

    if request.method == "POST":
        return redirect("/cars/setups")

    else:
        db = db_connection()
        cars = db.execute("SELECT * FROM cars").fetchall()
        return render_template("cars.html", cars=cars)


@app.route("/cars/setups", methods=["GET", "POST"])
def show_car_locations():
    if request.method == "POST":
        car_id = request.form.get("car_id")

        db = db_connection()
        # Get car brand and model
        car = db.execute("SELECT * FROM cars WHERE id=?", car_id).fetchone()
        # Use fetchone() to manipulate the object returned from query above
        # car = db.fetchall() //no use

        print(car["brand"])

        # Get available locations for current car
        car_locations = db.execute("SELECT DISTINCT locations.id AS location_id, location_name, location_image FROM locations INNER JOIN setups ON locations.id=setups.locations_id INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        return render_template ("setups.html", car_locations=car_locations, car=car)

    else:
        db = db_connection()
        cars = db.execute("SELECT * FROM cars")
        return render_template("cars.html", cars=cars)


@app.route("/cars/setups/setup", methods=["GET", "POST"])
def show_setup():
    """Show setup"""
    if request.method == "POST":
        location_id = request.form.get("location_id")
        car_id = request.form.get("car_id")

        db = db_connection()
        car = db.execute("SELECT brand, model, class FROM cars INNER JOIN setups ON cars.id=setups.cars_id WHERE setups.cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id]).fetchone()
        # car = db.fetchall()

        location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id]).fetchone()

        # locate = location[0]["location_name"]
        # print(location[0]["location_name"])
        # location = db.fetchall()

        # car_setups = db.execute("SELECT * FROM setups INNER JOIN locations ON setups.locations_id=locations.id WHERE locations.id IN (SELECT id FROM locations WHERE location_name=location) INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        car_setups = db.execute("SELECT * FROM setups WHERE cars_id=? and locations_id=?", [car_id, location_id])

        return render_template("car-setup.html", car_setups=car_setups, location=location, car=car)

    else:
        return render_template("index.html")


@app.route("/locations")
def locations():
    """Show locations"""
    db = db_connection()
    locations = db.execute("SELECT * FROM locations")

    return render_template("locations.html", locations=locations)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmationPassword = request.form.get("confirmation")
        hash = generate_password_hash(password)

        db = db_connection()
        new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", [username, hash])
        session["user_id"] = new_user.fetchone()
        db.commit()
        db.close()

        return redirect("/")

    else:
        return render_template("register.html")

# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)