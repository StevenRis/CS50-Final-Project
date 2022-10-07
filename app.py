from flask import Flask, render_template, redirect, request, session, flash
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars")
def cars():
    """Show cars"""
    connection = sql.connect("database.db")
    connection.row_factory = sql.Row

    db = connection.cursor()
    cars = db.execute("SELECT * FROM cars")
    return render_template("cars.html", cars=cars)


@app.route("/locations")
def locations():
    """Show locations"""
    connection = sql.connect("database.db")
    connection.row_factory = sql.Row

    db = connection.cursor()
    locations = db.execute("SELECT * FROM locations")

    return render_template("locations.html", locations=locations)


@app.route("/focus-rs-01", methods=["GET", "POST"])
def show_setup():
    """Show setup"""
    if request.method == "POST":
        location_name = request.form.get("location_name")

        if location_name == 'Catamarca Province, Argentina':
            return render_template('locations.html')

    else:
        connection = sql.connect("database.db")
        connection.row_factory = sql.Row

        db = connection.cursor()
        brand = 'Ford'
        setups = db.execute("SELECT DISTINCT location_name, location_image FROM locations INNER JOIN setups ON locations.id=setups.locations_id INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE brand=?)", [brand])

        return render_template ("focus-rs-01.html", setups=setups)


# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)