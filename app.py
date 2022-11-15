import sqlite3
from tempfile import mkdtemp

from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
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
        print(type(user_id))

        db = db_connection()
        # show_favorite_setups = db.execute("SELECT * FROM setups inner JOIN cars on cars.id=setups.cars_id inner JOIN locations ON locations.id=setups.locations_id INNER JOIN favorite_setups ON setups.id=favorite_setups.setup_id WHERE favorite_setups.setup_id IN (SELECT setup_id FROM favorite_setups WHERE user_id=?)", [user_id])
        show_favorite_setups = db.execute("SELECT user_id, setup_id, surface, tyres, conditions FROM setups INNER JOIN favorite_setups ON setups.id=favorite_setups.setup_id INNER JOIN users ON users.id=favorite_setups.user_id WHERE user_id IN (SELECT id FROM users WHERE id=?)", [user_id]).fetchall()
        # show_favorite_setups = db.execute("select setup_id from favorite_setups where user_id=?", [user_id]).fetchall()
        print(show_favorite_setups)

        # car = session["setup"]
        # sql_list = str(tuple([key for key in car])).replace(',)', ')')
        # print(sql_list)

        # print(f'{username}')
        # print(session["setup"])

        # db = db_connection()
        # cars = db.execute("SELECT * FROM setups WHERE id IN {sql_list}".format(sql_list=sql_list))

        # show_favorite_setups = db.execute("SELECT * FROM setups INNER JOIN (SELECT user_id from favorite_setups WHERE user_id=?)", [user_id])
        # id_setup = db.execute("SELECT setup_id FROM favorite_setups WHERE user_id=?", [user_id]).fetchall()
        # show_favorite_setups = db.execute("SELECT setups.id FROM setups INNER JOIN favorite_setups ON setups.id=favorite_setups.setup_id WHERE favorite_setups.setup_id IN (SELECT setup_id FROM favorite_setups WHERE user_id=?)", [user_id]).fetchall()
        # show_favorite_setups = db.execute("SELECT * FROM setups INNER JOIN favorite_setups ON setups.id=favorite_setups.setup_id WHERE favorite_setups.setup_id IN (SELECT id FROM setups WHERE id=6)").fetchall()
        # show_favorite_setups = db.execute("SELECT * FROM setups INNER JOIN favorite_setups ON setups.id=favorite_setups.setup_id WHERE favorite_setups.setup_id IN (SELECT setup_id FROM favorite_setups WHERE user_id=?)", [user_id]).fetchall()




        # print(show_favorite_setups[0])
        # for i in x:
        #     print(f'SETUP ID - {i[4]}')



        # car = db.execute("SELECT brand, model, class FROM cars INNER JOIN setups ON cars.id=setups.cars_id WHERE setups.cars_id IN (SELECT id FROM cars WHERE id=?)", [car_id]).fetchone()

        # location = db.execute("SELECT location_name FROM locations INNER JOIN setups ON locations.id=setups.locations_id WHERE setups.locations_id IN (SELECT id FROM locations WHERE id=?)", [location_id]).fetchone()

        # car_setups = db.execute("SELECT * FROM setups WHERE cars_id=? and locations_id=?", [car_id, location_id])
        return render_template("account.html", username=username, cars=cars, setups=show_favorite_setups)


@app.route("/cars", methods=["GET", "POST"])
def cars():
    """Display cars"""
    if request.method == "GET":
        db = db_connection()
        cars = db.execute("SELECT * FROM cars").fetchall()

        return render_template("cars.html", cars=cars)

    else:
        # return redirect("/cars/setups")
        return render_template("setups.html")



@app.route("/cars/<model>", methods=["GET", "POST"])
def show_car_locations(model):
    """Display car's location that was clicked"""
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

            # Get car's id to use while queriing the location table
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
        setup_id = request.form.get("setup_id")

        if setup_id:
            # Define current user id
            user_id = session["user_id"]

            # Before adding the setup to favorite_setups table
            # check if the user already has this setup
            # Get the user id from favorite_setups table
            db = db_connection()
            user = db.execute("SELECT user_id FROM favorite_setups WHERE user_id=?", [user_id]).fetchone()
            # print(user[0])

            # Check if the user has this setup, he wants to add
            # display a message "You already have this setup in the favorites!"
            if user:
                setup = db.execute("SELECT setup_id FROM favorite_setups WHERE setup_id=?", [setup_id]).fetchone()
                if setup:
                    flash ("You already have this setup in the favorites!")
                else:
            # If the user doesn't have the setup
            # add this setup to favorite_setups table
            # and display message "Setup was succesfully added to favorites!"
                    db.execute("INSERT INTO favorite_setups (user_id, setup_id) VALUES (?, ?)", [user_id, setup_id])
                    db.commit()
                    flash ("Setup was succesfully added to favorites!")
                    db.close()
                    return redirect(request.url)

            if not user:
                db.execute("INSERT INTO favorite_setups (user_id, setup_id) VALUES (?, ?)", [user_id, setup_id])
                db.commit()
                flash ("Setup was succesfully added to favorites!")
                db.close()
            return redirect(request.url)
            # return redirect(request.url)

        else:
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

        # Commit changes on database
        db.commit() 
        db.close() # Close connection with database
        flash("Password was reset.")

        return redirect('/')

# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000, debug=True)
