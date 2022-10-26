from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

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
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
@login_required
def index():
    # Define current user by id from session
    user_id = session["user_id"]

    db = db_connection() #connect database
    username = db.execute("SELECT username FROM users WHERE id=?", [user_id]).fetchall()

    username = username[0]["username"]
    db.close()

    if user_id == 0:
        username = "Anonymous"

    print(f'\n\n{user_id}\n\n')

    return render_template("index.html", username=username)


@app.route("/home")
def home():
    username = "Anonymous"
    return render_template("index.html", username=username)


@app.route("/account/<username>", methods=["GET", "POST"])
def account(username):

    user_id = session["user_id"]

    db = db_connection()
    username = db.execute("SELECT username FROM users WHERE id=?", [user_id]).fetchall()

    username = username[0]["username"]
    db.close()

    return render_template("account.html", username=username)


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

        location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id]).fetchone()

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

        # Check the username and password were submited
        if not username:
            flash("Please enter username")
            return redirect ('/apology')

        if not password:
            flash("Please enter password")
            return redirect ('/apology')

        # Check confirmation password is not empty
        if not confirmationPassword:
            flash("Please confirm the password")
            return redirect ('/apology')

        # Check password and the confrmation password are the same
        if confirmationPassword != password:
            flash("Passwords are not the same")
            return redirect ('/apology')

        db = db_connection()

        # Add user and password to database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", [username, hash])
            db.commit()
        except:
            # If username is already exists display error
            flash("User name already exists")
            return redirect ('/apology')

        # Get new user from database
        new_user = db.execute("SELECT id FROM users WHERE username=?", [username]).fetchone()
        db.close() #close connection with database

        # Remeber new user in session
        session["user_id"] = new_user["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check the username and password were submited
        if not username:
            flash("Please provide username")
            return redirect ('/apology')

        elif not password:
            flash("Please provide password", 403)
            return redirect ('/apology')

        db = db_connection() # Connect database
        # Query database for username
        users = db.execute("SELECT * FROM users WHERE username=?", [username]).fetchall()

        # Check username and password are correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], password):
            flash("Invalid username and/or password")
            return redirect ('/apology')

        db.close() # Close connection with database

        # Remember which user has logged in
        session["user_id"] = users[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/apology")
def apology():
    return render_template('apology.html')


@app.route("/password_reset", methods=["GET", "POST"])
def reset():
    """Reset password"""
    if request.method == "GET":
        return render_template("password_reset.html")

    else:
        username = request.form.get("username")
        new_password = request.form.get("new_password")
        confirmationPassword = request.form.get("confirmation")
        hash = generate_password_hash(new_password)

        # Check the username and password were submited
        if not username:
            flash("Please enter username")
            return redirect ('/apology')

        if not new_password:
            flash("Please enter password")
            return redirect ('/apology')

        # Check confirmation password is not empty
        if not confirmationPassword:
            flash("Please confirm the password")
            return redirect ('/apology')

        # Check password and the confrmation password are the same
        if confirmationPassword != new_password:
            flash("Passwords are not the same")
            return redirect ('/apology')

        db = db_connection() # Connect database
        user_id = db.execute("SELECT id FROM users WHERE username=?", [username]).fetchone()["id"] # Get user id from database

        # print(f'\n\n{user_id}\n\n')
        # Updata password
        db.execute("UPDATE users SET hash=? WHERE id=?", [hash, user_id])
        db.commit() # Commit changes
        db.close() # Close connection with database
        flash("Password was reset.")


        return redirect('/')

# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)