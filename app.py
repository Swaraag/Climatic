from flask import Flask, render_template, request, redirect, session
import sqlite3
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd
import numpy as np


app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "super secreto key"


con = sqlite3.connect('climatic.db', check_same_thread=False)

climatic = con.cursor()

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Please enter a username"
            return render_template("login.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "Please enter a passwoord"
            return render_template("login.html", error=error)

        # Query database for username
        climatic.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows = climatic.fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1:
            error = "Please enter existing username"
            return render_template("login.html", error=error)

        if not check_password_hash(rows[0][2], request.form.get("password")):
            error = "Please make sure password is correct"
            return render_template("login.html", error=error)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        print(session["user_id"])
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    #User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "Please enter a username"
            return render_template("register.html", error=error)

        # Ensure the password was submitted
        elif not request.form.get("password"):
            error = "Please enter a password"
            return render_template("register.html", error=error)

        elif not request.form.get("confirmation"):
            error = "Please enter your password again"
            return render_template("register.html", error=error)

        elif not request.form.get("confirmation") == request.form.get("password"):
            error = "Please provide the same password and confirmation"
            return render_template("register.html", error=error)
        
        hashed_password = generate_password_hash(request.form.get("password"))

        perms = "poster"
        
        
        climatic.execute("INSERT INTO users (username, hash, perms) VALUES (?, ?, ?)", (request.form.get("username"), hashed_password, perms))
        con.commit()

        # Remember which user has logged in
        climatic.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        session["user_id"] = climatic.fetchall()[0]
        
        #Redirect user to the home page
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/initiatives", methods=["GET"])
def initiatives():
    return render_template("initiatives.html")

@app.route("/takeaction", methods=["GET"])
def takeAction():
    return render_template("takeaction.html")


@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    return render_template("forecast.html")