from flask import Flask, render_template, redirect, request, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars")
def cars():
    return render_template("cars.html")


# enable debug mode - no need to restart the server to refresh the page
# python app.py - run the server
if __name__ == '__main__':
    app.run(debug=True)