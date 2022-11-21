import sqlite3
from tempfile import mkdtemp

from flask import (Flask, flash, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_session import Session
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


# Define current user from session
def define_user():
    user_id = session["user_id"]
    db = db_connection()
    username = db.execute("SELECT username FROM users WHERE id=?", [user_id]).fetchall()[0]["username"]
    db.close()
    return username


@app.route("/")
@login_required
def index():
    username = define_user()
    return render_template("index.html", username=username)


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "GET":

        username = define_user()
        user_id = session["user_id"]

        db = db_connection()

        show_favorite_setups = db.execute("SELECT user_id, setup_id, surface, tyres, conditions, brand, model, car_image, location_name, location_image FROM setups INNER JOIN favorite_setups ON setups.id=favorite_setups.setup_id INNER JOIN cars ON cars.id=setups.cars_id INNER JOIN locations ON locations.id=setups.locations_id INNER JOIN users ON users.id=favorite_setups.user_id WHERE user_id IN (SELECT id FROM users WHERE id=?)", [user_id]).fetchall()

        return render_template("account.html", user_id=user_id, username=username, cars=cars, setups=show_favorite_setups)

    else:
        # POST
        # Get user_id and setup_id
        user_id = request.form.get("user_id")
        setup_id = request.form.get("setup_id")

        # Init db connection
        db = db_connection()

        # Select user_id and setup_id from favorite_setups table
        # which setup to delete when user click delete button
        db.execute("DELETE FROM favorite_setups WHERE user_id=? AND setup_id=?", [user_id, setup_id])
        db.commit()
        flash("Setup was successfully deleted.")

        return redirect(url_for('account'))


@app.route("/account/favorite_setup/<model>/<location>", methods=["GET", "POST"])
@login_required
def show_fav_setups(model, location):
    """Display user's favorite setups"""

    # Display car setup when user clicks show button
    if request.method == "POST":
        model = request.form.get("model")
        location_name = request.form.get("location_name")
        setup_id = request.form.get("setup_id")

        db = db_connection()
        car_id = db.execute("SELECT id FROM cars WHERE model=?", [model]).fetchone()[0]
        location_id = db.execute("SELECT id FROM locations WHERE location_name=?", [location_name]).fetchone()[0]

        car = db.execute("SELECT brand, model, class FROM cars INNER JOIN setups ON cars.id=setups.cars_id WHERE setups.cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id]).fetchone()

        location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id]).fetchone()

        car_setups = db.execute("SELECT * FROM setups WHERE id=?", [setup_id])

        return render_template("car-setup.html", model=model, car_setups=car_setups, location=location, car=car)

    else:
        # Get
        return redirect("/account")



@app.route("/cars")
def cars():
    """Display cars"""
    db = db_connection()
    cars = db.execute("SELECT * FROM cars").fetchall()

    return render_template("cars.html", cars=cars)


@app.route("/cars/<model>", methods=["GET", "POST"])
def show_car_locations(model):
    """Display car's location that user clicked"""
    if request.method == "POST":
        # Get car's id from the car card
        # that was clicked
        car_id = request.form.get("car_id")

        db = db_connection()
        # Get car's data for current car
        car = db.execute("SELECT * FROM cars WHERE id=?", car_id).fetchone()

        # Get available locations for current car
        car_locations = db.execute("SELECT DISTINCT locations.id AS location_id, location_name, location_image FROM locations INNER JOIN setups ON locations.id=setups.locations_id INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        return render_template ("setups.html", car_locations=car_locations, car=car)

    else:
        # When user reach route via GET (as by clicking a link or via redirect)
        # define the current car from the link by getting the model from url
        db = db_connection()

        # Check the model exists in the database
        try:
            car = db.execute("SELECT * FROM cars WHERE model=?", [model]).fetchone()

            # Get car's id to use while quering the location table
            car_id = car['id']
        except:
            # If model from the url doesn't exist in the dabase
            # then display flash message
            # and display the apology page
            flash("There's no such car you are looking for!")
            return redirect("/apology")


        # Get locations that are available for the current car
        # which will be displayed to the user
        # by using the car_id
        car_locations = db.execute("SELECT DISTINCT locations.id AS location_id, location_name, location_image FROM locations INNER JOIN setups ON locations.id=setups.locations_id INNER JOIN cars ON cars.id=setups.cars_id WHERE cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id])

        return render_template("setups.html", car=car, model=model, car_locations=car_locations)


@app.route("/cars/<model>/<location>", methods=["GET", "POST"])
def show_setup(model, location):
    """Show setup"""
    if request.method == "POST":

        # Get the setup id when the user adds the setup to favorites
        setup_id = request.form.get("setup_id")
        if setup_id:
            # Define current user id
            user_id = session["user_id"]

            # Before adding the setup to favorite_setups table
            # check if the user already has this setup in favorites
            # Get the user_id and setup_id from favorite_setups table
            db = db_connection()
            exists = db.execute("SELECT EXISTS (SELECT 1 FROM favorite_setups WHERE user_id=? and setup_id=?)", [user_id, setup_id]).fetchone()[0]

            # In order to avoid duplication check the user has this setup, he wants to add
            # If the user doesn't have the setup
            # insert this setup to favorite_setups table
            # and display the message "Setup was successfully added to favorites!"
            if exists == 0:
                db.execute("INSERT INTO favorite_setups (user_id, setup_id) VALUES (?, ?)", [user_id, setup_id])
                db.commit()
                flash('Setup was added')

            else:
                # if has - display the message "You already have this setup in the favorites!"
                flash('You already have this setup in favorites')

            return redirect(request.url)

        else:
            # GET
            # Show setups for current car and location
            location_id = request.form.get("location_id")
            car_id = request.form.get("car_id")

            db = db_connection()
            car = db.execute("SELECT brand, model, class FROM cars INNER JOIN setups ON cars.id=setups.cars_id WHERE setups.cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id]).fetchone()

            location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id]).fetchone()

            car_setups = db.execute("SELECT * FROM setups WHERE cars_id=? and locations_id=?", [car_id, location_id])

            return render_template("car-setup.html", car_setups=car_setups, location=location, car=car)

    else:
        db = db_connection()
        # Check the model exists in the database
        try:
            car = db.execute("SELECT * FROM cars WHERE model=?", [model]).fetchone()
            loc = db.execute("SELECT * FROM locations WHERE location_name=?", [location]).fetchone()
            # Get car's id to use while queriing the location table
            car_id = car['id']
            location_id = loc["id"]
            location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id]).fetchone()
        except:
            # If model from the url doesn't exist in the dabase
            # then display flash message
            # and display the apology page
            flash("There's no such location you are looking for!")
            return redirect("/apology")

        car_setups = db.execute("SELECT * FROM setups WHERE cars_id=? and locations_id=?", [car_id, location_id])

        return render_template("car-setup.html", car=car, model=model, car_setups=car_setups, location=location)


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

        # Add user and password to database
        db = db_connection()
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

        flash(f"Hi {username}! You were successfully registered!")
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

        flash("You were successfully logged in!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/apology")
def apology():
    '''Display error page'''
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

        # Update password
        db.execute("UPDATE users SET hash=? WHERE id=?", [hash, user_id])

        # Commit changes on database
        db.commit() 
        db.close()
        flash("Password was reset.")

        return redirect('/')

# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)
