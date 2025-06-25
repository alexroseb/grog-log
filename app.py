from flask import Flask, render_template, session, json, request, redirect, flash
import csv
import os
from psycopg2 import pool
from dotenv import load_dotenv

app = Flask(__name__)

# Database setup
# Load .env file
load_dotenv()
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
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<id>")
def drink_info(id):
    con = connection_pool.getconn()
    cur = con.cursor()
    cur.execute("SELECT * FROM drinks WHERE id = "+ id)
    drink_info = cur.fetchall()
    print(drink_info)
    # Close the cursor and return the connection to the pool
    cur.close()
    connection_pool.putconn(con)
    if len(drink_info)>0:
        ingredients = drink_info[0][2].split(",")
        return render_template("drink_details.html", id=drink_info[0][0], name=drink_info[0][1], ingredients=ingredients)
    else:
        return render_template("drink_details.html", id=id, name="No drink found", ingredients=[])
    
@app.route("/signup")
def signup():
    con = connection_pool.getconn()
    cur = con.cursor()


    # Close the cursor and return the connection to the pool
    cur.close()
    connection_pool.putconn(con)