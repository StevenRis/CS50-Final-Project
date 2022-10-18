from flask import Flask, render_template, redirect, request, session, flash
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars", methods=["GET", "POST"])
def cars():
    """Show cars"""
    if request.method == "POST":
        return redirect("/cars/setups")

    else:
        connection = sql.connect("database.db")
        connection.row_factory = sql.Row

        db = connection.cursor()
        cars = db.execute("SELECT * FROM cars")
        return render_template("cars.html", cars=cars)


@app.route("/cars/setups", methods=["GET", "POST"])
def show_car_locations():
    """Show setup"""
    if request.method == "POST":
        car_id = request.form.get("car_id")

        connection = sql.connect("database.db")
        connection.row_factory = sql.Row

        db = connection.cursor()

        # Get car brand and model
        car = db.execute("SELECT * FROM cars WHERE id=?", car_id)
        # Use fetchone() to manipulate the object returned from query above
        car = db.fetchone()

        # Get available locations for current car
        car_locations = db.execute("SELECT DISTINCT locations.id AS location_id, location_name, location_image FROM locations INNER JOIN setups ON locations.id=setups.locations_id INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        return render_template ("setups.html", car_locations=car_locations, car=car)

    else:
        connection = sql.connect("database.db")
        connection.row_factory = sql.Row

        db = connection.cursor()
        cars = db.execute("SELECT * FROM cars")
        return render_template("cars.html", cars=cars)


@app.route("/cars/setups/setup", methods=["GET", "POST"])
def show_setup():
    if request.method == "POST":
        location_id = request.form.get("location_id")
        car_id = request.form.get("car_id")

        connection = sql.connect("database.db")
        connection.row_factory = sql.Row

        db = connection.cursor()

        # car = db.execute("SELECT * FROM cars WHERE id=?", car_id)
        # car = db.fetchone()

        # car_locations = db.execute("SELECT DISTINCT location_name, location_image FROM locations INNER JOIN setups ON locations.id=setups.locations_id INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        car = db.execute("SELECT brand, model, class FROM cars INNER JOIN setups ON cars.id=setups.cars_id WHERE setups.cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])
        car = db.fetchone()

        location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id])
        location = db.fetchone()

        # car_setups = db.execute("SELECT * FROM setups INNER JOIN locations ON setups.locations_id=locations.id WHERE locations.id IN (SELECT id FROM locations WHERE location_name=location) INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        car_setups = db.execute("SELECT * FROM setups WHERE cars_id=? and locations_id=?", [car_id, location_id])

        return render_template("car-setup.html", car_setups=car_setups, location=location, car=car)

    else:
        return render_template("index.html")


@app.route("/locations")
def locations():
    """Show locations"""
    connection = sql.connect("database.db")
    connection.row_factory = sql.Row

    db = connection.cursor()
    locations = db.execute("SELECT * FROM locations")

    return render_template("locations.html", locations=locations)


# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)