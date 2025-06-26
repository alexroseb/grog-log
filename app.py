from flask import Flask, render_template, session, json, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os
from psycopg2 import pool
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Database setup
# Get the connection string from the environment variable
connection_string = os.getenv('DATABASE_URL')
# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    1,  # Minimum number of connections in the pool
    10,  # Maximum number of connections in the pool
    connection_string
)
# Check if the pool was created successfully
if connection_pool:
    print("Connection pool created successfully")


@app.route("/")
def index():
    return render_template("index.html")

# Drinks information page
@app.route("/drink/<id>")
def drink_info(id):
    con = connection_pool.getconn()
    cur = con.cursor()
    cur.execute("SELECT * FROM drinks WHERE id = "+ id)
    drink_info = cur.fetchall()
    cur.close()
    connection_pool.putconn(con)
    if len(drink_info)>0:
        ingredients = drink_info[0][2].split(",")
        return render_template("drink_details.html", id=drink_info[0][0], name=drink_info[0][1], ingredients=ingredients)
    else:
        return render_template("drink_details.html", id=id, name="No drink found", ingredients=[])

## Auth section ##
@app.route("/signup")
def signup():
    return render_template("signup.html", error="")

@app.route('/signup', methods=['POST'])
def signup_post():
    con = connection_pool.getconn()
    cur = con.cursor()

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if " " in username:
        return render_template("signup.html", error="Please do not include spaces in your username")

    cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))
    user_info = cur.fetchall()
    if len(user_info)>0:
        return render_template("signup.html", error="Username already exists")
    
    cur.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    user_info = cur.fetchall()
    if len(user_info)>0:
        return render_template("signup.html", error="Email already exists")

    cur.execute("INSERT INTO users(username, email, password) VALUES('{}','{}','{}')".format(username, email, generate_password_hash(password, method='scrypt')))
    con.commit()

    cur.close()
    connection_pool.putconn(con)
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html", error="")

@app.route('/login', methods=['POST'])
def login_post():
    con = connection_pool.getconn()
    cur = con.cursor()

    email_or_user = request.form.get('email')
    password = request.form.get('password')

    cur.execute("SELECT username, password FROM users WHERE username = '{}'".format(email_or_user))
    user_info = cur.fetchall()
    if len(user_info)>0:
        if check_password_hash(user_info[0][1], password):
            session["logged_in"] = True
            session["user"] = user_info[0][0]
            return redirect("/profile")
        else:
            return render_template("/login", error="Password incorrect.")
    
    cur.execute("SELECT username, password FROM users WHERE email = '{}'".format(email_or_user))
    user_info = cur.fetchall()
    if len(user_info)>0:
        if check_password_hash(user_info[0][1], password):
            session["logged_in"] = True
            session["user"] = user_info[0][0]
            return redirect("/profile")
        else:
            return render_template("/login", error="Password incorrect.")
    cur.close()
    connection_pool.putconn(con)
    return render_template("/login", error="User does not exist.")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    session["user"] = ""
    return redirect("/")

@app.route("/profile")
def profile():
    if (session.get('logged_in') and session["logged_in"] and session.get('user')):
        return redirect("/user/"+session["user"])
    else:
        return redirect("/login")

# User log page
@app.route("/user/<username>")
def user_page(username):
    con = connection_pool.getconn()
    cur = con.cursor()
    cur.execute("SELECT drink_log, public FROM users WHERE username = '{}'".format(username))
    user_info = cur.fetchall()
    print(user_info)
    cur.close()
    connection_pool.putconn(con)
    if len(user_info)>0:
        if (user_info[0][1] or (session.get('logged_in') and session.get('user') and session['logged_in'] and session['user']==username)):
            return render_template("user.html", drink_log=user_info[0][0], hasData=True, username=username, public=user_info[0][1])
        else:
            return render_template("user.html", hasData=False, username=username)
    else:
        return render_template("user.html", hasData=False, username="User does not exist")